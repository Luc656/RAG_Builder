def format_context(chunks):

    context = ''
    for i, chunk in enumerate(chunks):
        title = chunk.get('title', None)
        source = chunk.get('source', None)
        text  = chunk['text']
        context += f"### Chunk {i+1}\nTitle: {title}\nSource: {source}\nContent: {text}\n\n"
    return context

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

# todo: send prompt to LLM