import weaviate
from sentence_transformers import SentenceTransformer
from processor import Processor

#pipeline = Processor()

# make this inherited ???
class Retriever(Processor):

    def __init__(self, client):
        self.client = client
        self.results = None
        self.context = None
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
        self.results = result['data']['Get']['DocumentChunk']

    #@staticmethod
    def format_context(self):

        context = ''
        for i, chunk in enumerate(self.results):
            title = chunk.get('title', None)
            source = chunk.get('source', None)
            text = chunk['text']
            context += f"### Chunk {i + 1}\nTitle: {title}\nSource: {source}\nContent: {text}\n\n"
        self.context = context

    #@staticmethod
    def build_prompt(self):
        prompt = f"""
        You are a helpful assistant. Use the context below to answer the question. Answer in terms of travel only.

        Context:
        ---------
        {self.context}
        ---------

        Question: {self.doc_body}

        Answer:
        """
        return prompt

        # embed user query
