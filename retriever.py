import weaviate
from sentence_transformers import SentenceTransformer
from processor import Processor

#pipeline = Processor()

# make this inherited ???
class Retriever(Processor):

    def __init__(self, client):
        self.client = client
        super().__init__()

    def retrieve_chunks(self, query, k=5, metadata_filter=None):

        self.doc_body = query

        self.split_text()
        self.transform()

        query_builder = self.client.query.get("DocumentChunk", ["text", "title", "tags", "source"])

        query_builder = query_builder.with_near_vector({
            'vector': self.embeddings.tolist()
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
