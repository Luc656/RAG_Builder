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
        self.weaviate_client = weaviate.WeaviateClient(
            connection_params=weaviate.connect.ConnectionParams.from_url(
                url=weaviate_url,
                grpc_port=weaviate_grpc_port
            )
        )

    def split_text(self, max_tokens=200):

        # if len(self.doc_body) > 1:
        #     ' '.join(self.doc_body)

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
        # Check if collection exists and create if it doesn't
        try:
            # Try to get the collection (will raise exception if not found)
            collection = self.weaviate_client.collections.get(self.class_name)
        except weaviate.exceptions.WeaviateQueryError:
            # Create the collection with the schema
            collection = self.weaviate_client.collections.create(
                name=self.class_name,
                properties=[
                    weaviate.Property(name="text", data_type=weaviate.DataType.TEXT),
                    weaviate.Property(name="title", data_type=weaviate.DataType.TEXT),
                    weaviate.Property(name="url", data_type=weaviate.DataType.TEXT),
                    weaviate.Property(name="tags", data_type=weaviate.DataType.TEXT_ARRAY),
                    weaviate.Property(name="source", data_type=weaviate.DataType.TEXT),
                    weaviate.Property(name="created_at", data_type=weaviate.DataType.DATE)
                ],
                vectorizer_config=None  # Equivalent to "vectorizer": "none" in v3
            )
        else:
            # If no exception, collection exists
            collection = self.weaviate_client.collections.get(self.class_name)

        # Create a list of objects to insert in batch
        objects_to_insert = []

        for i, (chunk, vector) in enumerate(zip(self.chunks, self.embeddings)):
            objects_to_insert.append({
                "properties": {
                    "text": chunk,
                    "title": "RAG Overview",
                    "tags": [],  # TODO: this
                    "source": "internal_notes.md",
                    "created_at": datetime.now().isoformat()
                },
                "vector": vector.tolist()
            })

        # Use batch insertion for better performance
        with collection.batch.dynamic() as batch:
            for obj in objects_to_insert:
                batch.add_object(
                    properties=obj["properties"],
                    vector=obj["vector"]
                )

        print('chunks successfully uploaded!')

