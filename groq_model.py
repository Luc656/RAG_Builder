from groq import Groq
import os

api_key = os.environ.get("GROQ_API_KEY") # TODO: get KEY again in env
#print(api_key)

def groq_talk(prompt, key):

    client = Groq(
        api_key=key
    )

    chat = client.chat.completions.create(
        messages=[
            {
                "role":"user",
                "content":f"{prompt}"
            }
        ],
        model="llama-3.3-70b-versatile",
        stream=False
    )

    print(chat)
    print(chat.choices[0].message.content)

    return chat.choices[0].message.content



    # define which index search used to return correct embeddings