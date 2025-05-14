import weaviate
from sentence_transformers import SentenceTransformer
from blog_pipeline_v2 import Pipeline

pipeline = Pipeline()

# make this inherited ???
class RAG:

    def __init__(self):
        pass

    def retreive_chunks(self, query, k=5, metadata_filter=None):

        user_query = pipeline.split_text(query)
        user_query = pipeline.transform(user_query)

        query_builder = client.query.get("DocumentChunk", ["text", "title", "tags", "source"])

        query_builder = query_builder.with_near_vector({
            'vector': user_query.tolist()
        }).with_limit(k)

        if metadata_filter:
            query_builder = query_builder.with_where(metadata_filter)

        result = query_builder.do()
        return result['data']['Get']['DocumentChunk']



        # embed user query
