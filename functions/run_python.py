import os
import subprocess

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

