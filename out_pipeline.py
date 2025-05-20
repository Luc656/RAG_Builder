from processor import Processor
from retriever import Retriever
from blog_scraper_simple import WebScraper
from groq_model import api_key, groq_talk

# steps:
#   1. accept query
#   2. retrieve data
#   3. format response & build prompt
#   4. send to LLM

def out_pipeline():

    user_query = input('How can I help you today?')

    retriever = Retriever()

    retriever.retrieve_chunks()
    retriever.format_context()
    prompt = retriever.build_prompt()

    message = groq_talk(prompt, api_key)

    print(message)


