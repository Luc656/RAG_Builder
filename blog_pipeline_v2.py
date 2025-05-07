import re
from sentence_transformers import SentenceTransformer
import weaviate
from datetime import datetime
from weaviate.classes.init import AdditionalConfig

class Pipeline:

    def __init__(self,
                 doc_body,
                 doc_title,
                 doc_tags,
                 doc_url,
                 embed_model='all-MiniLM-L6-v2',
                 weaviate_url='http://localhost:8080',
                 weaviate_grpc_port=50051,  # Default gRPC port for Weaviate
                 class_name='DocChunk'):

        self.doc_body = doc_body
        self.doc_title = doc_title
        self.doc_tags = doc_tags
        self.doc_url = doc_url
        self.doc_created_at = None
        self.embed_model = SentenceTransformer(embed_model)
        #self.weaviate_client = weaviate.Client(weaviate_url)
        self.class_name = class_name
        self.chunks = None # each instance can only hold & transform one article?
        self.embeddings = None
        self.weaviate_url = weaviate_url
        # self.weaviate_client = weaviate.WeaviateClient(
        #     connection_params=weaviate.connect.ConnectionParams.from_url(
        #         url=weaviate_url,
        #         grpc_port=weaviate_grpc_port
        #     )
        # )

    def split_text(self, max_tokens=200):

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

    def insert(self):
        # Connect to a local Weaviate instance
        client = weaviate.connect_to_custom(
            http_host="localhost",
            http_port=8080,
            http_secure=False,  # This is needed
            grpc_host="localhost",
            grpc_port=50051,
            grpc_secure=False,
            #additional_config=AdditionalConfig(timeout=30)
        )

        # # Ensure doc_body is chunked
        # if not self.chunks:
        #     self.chunks = self.chunk_text(self.doc_body)  # You need to implement this

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