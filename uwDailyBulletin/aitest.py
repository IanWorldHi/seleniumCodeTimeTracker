import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


chatgptkey = os.getenv("CHATGPTKEY")
client = OpenAI(api_key=chatgptkey)


response = client.responses.create(
    model="gpt-4.1-mini",
    input="What model is best to call with an api key for a notificatio service that is parsed by chatgpt to send to only the appriopriate users"
)

print(response.output_text)











