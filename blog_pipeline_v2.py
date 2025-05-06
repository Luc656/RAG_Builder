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
        from datetime import datetime
        import weaviate
        from weaviate.embedded import EmbeddedOptions

        # Parse URL components safely
        parsed_url = urllib.parse.urlparse(self.weaviate_url)
        secure = parsed_url.scheme == 'https'
        host = parsed_url.hostname or 'localhost'
        port = parsed_url.port or (443 if secure else 80)

        # For v4.x - Create client with Connection object
        # This approach doesn't use the deprecated 'rest' module
        if self.weaviate_url.startswith("http"):
            # For remote Weaviate
            # For remote Weaviate
            # Weaviate requires different ports for HTTP and gRPC
            # Typically gRPC port is HTTP port + 1 (e.g., 8080 for HTTP, 8081 for gRPC)
            grpc_port = port + 1  # Default convention: gRPC port = HTTP port + 1

            client = weaviate.connect_to_custom(
                http_host=host,
                http_port=port,
                http_secure=secure,
                grpc_host=host,
                grpc_port=grpc_port,  # Must be different from HTTP port
                grpc_secure=secure
                # If you need authentication:
                # auth_credentials=weaviate.auth.AuthApiKey(api_key="your-api-key")
            )
        else:
            # For embedded/local Weaviate
            client = weaviate.connect_to_embedded(
                options=EmbeddedOptions()
            )

        try:
            # Check if collection exists - v4.x style
            try:
                collection = client.collections.get(self.class_name)
                print(f"Collection {self.class_name} exists")
            except weaviate.exceptions.WeaviateQueryError:
                # Create collection if it doesn't exist - v4.x style
                print(f"Creating collection {self.class_name}")
                collection = client.collections.create(
                    name=self.class_name,
                    properties=[
                        weaviate.classes.properties.Property(name="text",
                                                             data_type=weaviate.classes.properties.DataType.TEXT),
                        weaviate.classes.properties.Property(name="title",
                                                             data_type=weaviate.classes.properties.DataType.TEXT),
                        weaviate.classes.properties.Property(name="url",
                                                             data_type=weaviate.classes.properties.DataType.TEXT),
                        weaviate.classes.properties.Property(name="tags",
                                                             data_type=weaviate.classes.properties.DataType.TEXT_ARRAY),
                        weaviate.classes.properties.Property(name="source",
                                                             data_type=weaviate.classes.properties.DataType.TEXT),
                        weaviate.classes.properties.Property(name="created_at",
                                                             data_type=weaviate.classes.properties.DataType.DATE)
                    ],
                    vectorizer_config=weaviate.classes.config.Configure.Vectorizer.none()
                )

            # Perform batch insertion - v4.x style
            with collection.batch.dynamic() as batch:
                for i, (chunk, vector) in enumerate(zip(self.chunks, self.embeddings)):
                    try:
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
                    except Exception as e:
                        print(f"Error adding object {i}: {e}")

            print(f"{len(self.chunks)} chunks successfully uploaded!")

        finally:
            # Close the client connection in v4.x
            client.close()


