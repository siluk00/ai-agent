import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
content = client.models.generate_content(model="gemini-2.0-flash-001",contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
print(content.text)
prompt_usage = content.usage_metadata
print(f"Prompt tokens: {prompt_usage.prompt_token_count}")
print(f"Response tokens: {prompt_usage.candidates_token_count}")