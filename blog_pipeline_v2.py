import re
from sentence_transformers import SentenceTransformer
import weaviate
from datetime import datetime

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
        """Insert document chunks using a short-lived connection,minimum resource usage for isolated ops, more conn overhead"""
        import urllib.parse

        # Parse URL components safely
        parsed_url = urllib.parse.urlparse(self.weaviate_url)
        secure = parsed_url.scheme == 'https'
        host = parsed_url.hostname or 'localhost'
        port = parsed_url.port or (443 if secure else 80)

        # Create connection params for v4.14.1
        connection_params = weaviate.connect.rest.ConnectionParams(
            host=host,
            port=port,
            secure=secure
        )

        # Use context manager for automatic connection management
        with weaviate.WeaviateClient(connection_params=connection_params) as client:
            # Check if collection exists
            try:
                collection = client.collections.get(self.class_name)
            except weaviate.exceptions.WeaviateQueryError:
                # Create collection if it doesn't exist
                collection = client.collections.create(
                    name=self.class_name,
                    properties=[
                        weaviate.Property(name="text", data_type=weaviate.DataType.TEXT),
                        weaviate.Property(name="title", data_type=weaviate.DataType.TEXT),
                        weaviate.Property(name="url", data_type=weaviate.DataType.TEXT),
                        weaviate.Property(name="tags", data_type=weaviate.DataType.TEXT_ARRAY),
                        weaviate.Property(name="source", data_type=weaviate.DataType.TEXT),
                        weaviate.Property(name="created_at", data_type=weaviate.DataType.DATE)
                    ],
                    vectorizer_config=None
                )

            # Perform batch insertion
            with collection.batch.dynamic() as batch:
                for chunk, vector in zip(self.chunks, self.embeddings):
                    batch.add_object(
                        properties={
                            "text": chunk,
                            "title": self.doc_title,
                            "tags": self.doc_tags,
                            "url": self.doc_url,
                            "source": self.doc_url.split('/')[-1] if self.doc_url else "unknown",
                            "created_at": datetime.now().isoformat()
                        },
                        vector=vector.tolist()
                    )

            print(f"{len(self.chunks)} chunks successfully uploaded!")


