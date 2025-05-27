from processor import Processor
from retriever import Retriever
from blog_scraper_simple import WebScraper
from groq_model import api_key, groq_talk
import weaviate

# steps:
#   1. accept query
#   2. retrieve data
#   3. format response & build prompt
#   4. send to LLM

client = weaviate.connect_to_custom(
            http_host="localhost",
            http_port=8080,
            http_secure=False,  # This is needed
            grpc_host="localhost",
            grpc_port=50051,
            grpc_secure=False,
            #additional_config=AdditionalConfig(timeout=30)
        )

def out_pipeline():

    user_query = input('How can I help you today?')

    retriever = Retriever(user_query=user_query, client=client)

    retriever.retrieve_chunks()
    retriever.format_context()
    prompt = retriever.build_prompt()

    message = groq_talk(prompt, api_key)

    print(message)


