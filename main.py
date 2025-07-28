import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.file_info import schema_get_files_info
from functions.file_info import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.file_info import get_file_content
from functions.file_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file


def call_function(function_call_part, verbose = False):
    fc = function_call_part.function_call
    if verbose:
        print(f"Calling function: {fc.name}({fc.args})")
    else:
        print(f" - Calling function: {fc.name}")
    function_dict = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if fc.name not in function_dict.keys():
        return types.Part.from_function_response(
            name=fc.name,
            response={"error": f"Unknown function: {fc.name}"},
        )
    
    mutable_args = dict(fc.args)
    if fc.name == 'run_python_file' and 'args' not in mutable_args:
        mutable_args['args'] = []

    mutable_args["working_directory"]="./calculator"
    
    try:
        result = function_dict[fc.name](
            **mutable_args
        )
        return types.Part.from_function_response(
            name = fc.name,
            response={"result": result},
        )
    except Exception as e:
        return types.Part.from_function_response(
            name=fc.name,
            response={"error": str(e)},
        )

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) > 3 or len(sys.argv) < 2:
    print("Usage: python your_script_name.py \"<prompt>\" [--verbose]")
    exit(1)
if len(sys.argv) == 3 and sys.argv[2] != "--verbose" :
    print("Usage: python your_script_name.py \"<prompt>\" [--verbose]")
    exit(1)

verbose = len(sys.argv) == 3 and sys.argv[2] == "--verbose"

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

messages = [types.Content(role="user", parts=[types.Part(text=sys.argv[1])])]


system_prompt = """
You are an autonomous AI coding agent. Your sole purpose is to answer questions about the code in the user's working directory by using the tools provided.

**CRITICAL INSTRUCTIONS:**
1.  **DO NOT** give up, apologize, or say you don't have enough information.
2.  Your first step for any question about the codebase is to use the `get_files_info` tool to see the project structure.
3.  Based on the file list, use `get_file_content` to read the relevant files.
4.  Form a step-by-step plan and execute it using your tools.
5.  Only provide the final answer once you have gathered all the necessary information from reading the files.
"""

MAX_ITERATIONS = 20
try:
    for i in range(MAX_ITERATIONS):
        print(f"\n--- Turn {i + 1} ---")
        
        response = client.models.generate_content(
            model="gemini-1.5-flash-latest",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions]
            )
        )
        
        if not response.candidates or not response.candidates[0].content.parts:
             print("Received an empty response from the model. Stopping.")
             break
        
        candidate = response.candidates[0]
        
        if candidate.content.parts[0].text:
            print("\n✅ Final Answer:")
            print(candidate.content.parts[0].text)
            if verbose:
                prompt_usage = response.usage_metadata
                print("\n--- Usage Metadata ---")
                print(f"Prompt tokens: {prompt_usage.prompt_token_count}")
                print(f"Response tokens: {prompt_usage.candidates_token_count}")
            break
        
        messages.append(candidate.content)

        function_responses = []
        for part in candidate.content.parts:
            if part.function_call:
                result_part = call_function(part, verbose)
                function_responses.append(result_part)
                if verbose:
                    print(f"-> {result_part.function_response.response}")
        
        messages.append(types.Content(role="tool", parts=function_responses))

    else:
        print(f"\n🚫 Reached maximum iterations ({MAX_ITERATIONS}). Stopping.")

except Exception as e:
    print(f"\nAn error occurred during the process: {e}")