# Import the Python SDK
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
# Used to securely store your API key
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

model={}
model["flash"] = genai.GenerativeModel('gemini-1.5-flash')
model["pro"] = genai.GenerativeModel('gemini-1.5-pro')

async def runModel(modelName, prompt):
    response = model[modelName].generate_content(
        prompt,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT : HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT : HarmBlockThreshold.BLOCK_NONE
        }
    )
    return response.text

def embed(content):
    return genai.embed_content(
    model="models/text-embedding-004",
    content=content,
    task_type="retrieval_document",
    title="Embedding of single string")['embedding']

if __name__ == "__main__":
    print(runModel("flash", "What is the capital of the moon?"))