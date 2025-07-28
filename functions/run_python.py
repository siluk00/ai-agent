import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)
        if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot execute "{file_path}" as it is outside'
        if not os.path.isfile(full_path):
            return f'Error: File "{file_path}" not found'
        if not file_path.endswith(".py"):
            return f'"{file_path}" is not a python file'
        stderr, stdout = "", ""
        output = subprocess.run(
                        ["python3", full_path] + args,
                        timeout=30,
                        capture_output=True,
                        cwd=working_directory + "/.."
                        )
        completed_process = f"STDOUT: {output.stdout}, SDTERR: {output.stderr}\n"
        if output.returncode:
            completed_process += f"Process exited with exit code {output.returncode}"
        if not output:
            return "No output produced"
        return completed_process
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file with the specified arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file that will be run. It's inside the scope of the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Array of string arguments that will be run. like command flags.",
                items=types.Schema(type=types.Type.STRING)
            )
        },
    ),
)