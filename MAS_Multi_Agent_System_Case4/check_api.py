from google import genai
import os
from dotenv import load_dotenv
load_dotenv()

os.environ['API_KEY'] = os.getenv('API_KEY')

client = genai.Client(api_key=os.environ['API_KEY'])

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works in a few words"
)
print(response.text)


