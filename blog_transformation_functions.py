# chunk & embedd
import re
from sentence_transformers import SentenceTransformer

######### 1. Chunk ###########

def split_text(text, max_tokens=200):

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

########## 2. Embed #########

def transform(chunks):

    model = SentenceTransformer('all-MiniLM-L6-v2')

    print('creating embeddings....')

    embeddings = model.encode(chunks, convert_to_tensor=True)

    return embeddings

