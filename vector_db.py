import weaviate

client = weaviate.Client('http://localhost:8080')

class_name = 'DocChunk'

if not client.schema.contains({'classes':[{'class':class_name}]}):
    client.schema.create_class({
        'class':class_name,
        'properties': [
            {'name': 'text', 'datatype': ['text']},
        ],
        'vectorIndexConfig': {},
        'vectorizer': 'none'
    })

for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
    client.data_object.create(
        data_object={'text': chunk},
        class_name=class_name,
        vector=vector.tolist()
    )

print('chunks successfully uploaded!')