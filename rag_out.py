import weaviate
from sentence_transformers import SentenceTransformer
from rag_in import Pipeline

pipeline = Pipeline()

# make this inherited ???
class Out(Pipeline):

    def __init__(self,client):
        self.client = client

    def retrieve_chunks(self, query, k=5, metadata_filter=None):

        user_query = pipeline.split_text(query)
        user_query = pipeline.transform(user_query)

        query_builder = self.client.query.get("DocumentChunk", ["text", "title", "tags", "source"])

        query_builder = query_builder.with_near_vector({
            'vector': user_query.tolist()
        }).with_limit(k)

        if metadata_filter:
            query_builder = query_builder.with_where(metadata_filter)

        result = query_builder.do()
        return result['data']['Get']['DocumentChunk']

    @staticmethod
    def format_context(chunks):

        context = ''
        for i, chunk in enumerate(chunks):
            title = chunk.get('title', None)
            source = chunk.get('source', None)
            text = chunk['text']
            context += f"### Chunk {i + 1}\nTitle: {title}\nSource: {source}\nContent: {text}\n\n"
        return context

    @staticmethod
    def build_prompt(context, user_query):
        prompt = f"""
        You are a helpful assistant. Use the context below to answer the question. Answer in terms of travel only.

        Context:
        ---------
        {context}
        ---------

        Question: {user_query}

        Answer:
        """
        return prompt

        # embed user query
