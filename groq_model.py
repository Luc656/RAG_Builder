from groq import Groq
import os

api_key = os.environ.get("GROQ_API_KEY")
print(api_key)

client = Groq(
    api_key=api_key
)

chat = client.chat.completions.create(
    messages=[
        {
            "role":"user",
            "content":"Tell me about Kyrgyzstan"
        }
    ],
    model="llama-3.3-70b-versatile",
    stream=False
)

print(chat)
print(chat.choices[0].message.content)