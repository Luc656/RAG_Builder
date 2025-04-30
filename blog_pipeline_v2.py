import re
from sentence_transformers import SentenceTransformer
import weaviate

class Pipeline:

    def __init__(self, embed_model='all-MiniLM-L6-v2', weaviate_client='http://localhost:8080',  class_name 'DocChunk'):
        self.embed_model = SentenceTransformer(embed_model)
        self.weaviate_client = weaviate.Client(weaviate_client)
        self.class_name = class_name


    def split_text(self, text, max_tokens=200):

        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks, curr_chunk = [], []

        curr_len = 0
        for i in sentences:
            sen_len = len(i.split())
            if curr_len + sen_len > max_tokens:
                chunks.append(' '.join(curr_chunk))
                curr_chunk = [i]
                curr_len = sen_len
            else:
                curr_chunk.append(i)
                curr_len += sen_len

        if curr_chunk:
            chunks.append(' '.join(curr_chunk))
        return chunks

    def transform(self, chunks):

        print('creating embeddings....')

        embeddings = self.embed_model.encode(chunks, convert_to_tensor=True)

        return embeddings

    def insert(self):



        if not self.weaviate_client.schema.contains({'classes': [{'class': self.class_name}]}):
            self.weaviate_client.schema.create_class({
                'class': self.class_name,
                'properties': [
                    {'name': 'text', 'datatype': ['text']},
                ],
                'vectorIndexConfig': {},
                'vectorizer': 'none'
            })

        for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
            self.weaviate_client.data_object.create(
                data_object={'text': chunk},
                class_name=self.class_name,
                vector=vector.tolist()
            )

        print('chunks successfully uploaded!')

