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
                 weaviate_client='http://localhost:8080',
                 class_name='DocChunk'):

        self.doc_body = doc_body
        self.doc_title = doc_title
        self.doc_tags = doc_tags
        self.doc_url = doc_url
        self.doc_created_at = None
        self.embed_model = SentenceTransformer(embed_model)
        self.weaviate_client = weaviate.Client(weaviate_client)
        self.class_name = class_name
        self.chunks = None

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

    def transform(self):

        print('creating embeddings....')

        embeddings = self.embed_model.encode(self.chunks, convert_to_tensor=True)

        return embeddings

    def insert(self):

        if not self.weaviate_client.schema.contains({'classes': [{'class': self.class_name}]}):
            self.weaviate_client.schema.create_class({
                'class': self.class_name,
                'properties': [
                    {'name': 'text', 'dataType': ['text']},
                    {'name': 'title', 'dataType': ['text']},
                    {'name': 'url', 'dataType': ['text']},
                    {'name': 'tags', 'dataType': ['text[]']},
                    {'name': 'created_at', 'dataType': ['date']}
                ],
                'vectorIndexConfig': {},
                'vectorizer': 'none'
            })

        for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
            self.weaviate_client.data_object.create(
                data_object={
                    "text": chunk,
                    "title": "RAG Overview",
                    "tags": [], #TODO: this
                    "source": "internal_notes.md",
                    "created_at": f"{datetime.now()}"
                },
                class_name="DocumentChunk",
                vector=vector.tolist()
            )

        print('chunks successfully uploaded!')

