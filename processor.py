import re
from sentence_transformers import SentenceTransformer
import weaviate
from datetime import datetime
from weaviate.classes.init import AdditionalConfig

# todo: should some of these be static ???
class Processor:

    def __init__(self,
                 doc_body,
                 # doc_title,
                 # doc_tags,
                 # doc_url,
                 embed_model='all-MiniLM-L6-v2',
                 weaviate_url='http://localhost:8080',
                 weaviate_grpc_port=50051,  # Default gRPC port for Weaviate
                 class_name='DocChunk'):

        self.doc_body = doc_body
        self.doc_title = None
        self.doc_tags = None
        self.doc_url = None
        self.doc_created_at = None
        self.embed_model = SentenceTransformer(embed_model)
        #self.weaviate_client = weaviate.Client(weaviate_url)
        self.class_name = class_name
        self.chunks = None # each instance can only hold & transform one article?
        self.embeddings = None
        self.weaviate_url = weaviate_url

    def chunk_document(self, chunk_size: int = 500,
                      overlap: int = 50):
        """
        Split document into overlapping chunks

        Args:
            text: Document text
            chunk_size: Target chunk size in characters
            overlap: Overlap between chunks

        Returns:
            List of text chunks
        """

        if len(self.doc_body) > 1: # body is list of <p> elements, join to 1 string to chunk
            self.doc_body = ' '.join(self.doc_body)

        # Clean the text
        text = re.sub(r'\s+', ' ', self.doc_body.strip())

        if len(text) <= chunk_size:
            return [text]

        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size

            # Try to break at sentence boundaries
            if end < len(text):
                # Look for sentence end within reasonable distance
                for i in range(min(100, chunk_size // 4)):
                    if end - i < len(text) and text[end - i] in '.!?':
                        end = end - i + 1
                        break

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            # Move start position with overlap
            start = end - overlap

        self.chunks = chunks

        print('chunks: ', self.chunks)


    # Todo: chunk metadata from blog, index in blog and total in blog
    def chunk_text(self, max_tokens=200):

        if len(self.doc_body) > 1: # body is list of <p> elements, join to 1 string to chunk
            self.doc_body = ' '.join(self.doc_body)

        #print('body', self.doc_body)
        sentences = re.split(r'(?<=[.!?])\s+', self.doc_body)
        self.chunks, curr_chunk = [], []

        curr_len = 0
        for i in sentences:
            sen_len = len(i.split())
            if curr_len + sen_len > max_tokens:
                self.chunks.append(' '.join(curr_chunk))
                curr_chunk = [i]
                curr_len = sen_len
            else:
                curr_chunk.append(i)
                curr_len += sen_len

        if curr_chunk:
            self.chunks.append(' '.join(curr_chunk))

        print('chunks: ', self.chunks)

    def transform(self):

        print('creating embeddings....')

        self.embeddings = self.embed_model.encode(self.chunks, convert_to_tensor=True)

        print('embeds: ', self.embeddings)

    # TODO: check this closes upon failure
    def insert(self):
        # Connect to a local Weaviate instance

        client = None

        try:
            client = weaviate.connect_to_custom(
                http_host="localhost",
                http_port=8080,
                http_secure=False,  # This is needed
                grpc_host="localhost",
                grpc_port=50051,
                grpc_secure=False,
                #additional_config=AdditionalConfig(timeout=30)
            )

            if not self.embed_model:
                raise ValueError('Embedding model not initialized.')
            if not self.doc_body:
                raise ValueError('Document body is empty.')

            # Ensure doc_body is chunked
            if not self.chunks:
                self.split_text(self.doc_body)

            # Generate embeddings
            self.embeddings = self.embed_model.encode(self.chunks).tolist()

            # Add each chunk
            for chunk, embedding in zip(self.chunks, self.embeddings):
                properties = {
                    "text": chunk,
                    "title": self.doc_title,
                    "tags": self.doc_tags,
                    "url": self.doc_url,
                    "source": self.doc_url.split('/')[-1] if self.doc_url else "unknown",
                    "created_at": datetime.now().isoformat()
                }

                client.collections.get(self.class_name).data.insert(
                    properties=properties,
                    vector=embedding
                )

        except Exception as e:
            print(f'Error {e} while inserting')

        finally:
            if client:
                client.close()