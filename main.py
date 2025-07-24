import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
if len(sys.argv)  > 3:
    exit(1)
if len(sys.argv) == 3 and sys.argv[2] != "--verbose" :
    exit(1)
messages = [types.Content(role="user", parts=[types.Part(text=sys.argv[1])])]
system_prompt='Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'
content = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt))
print(content.text)
if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
    prompt_usage = content.usage_metadata
    print(f"User prompt: {messages[0]}")
    print(f"Prompt tokens: {prompt_usage.prompt_token_count}")
    print(f"Response tokens: {prompt_usage.candidates_token_count}")

