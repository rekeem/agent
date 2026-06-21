
import os
import subprocess
from google.genai import types


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_path, file_path))
        if  not os.path.commonpath([working_path, target_file]) == working_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file]
        if args:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, text=True,timeout = 30)
        output = ""
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"
        if result.stdout == result.stderr =="":
            output += "No output produced.\n"
        else:
            if result.stdout:
                output += f"STDOUT: {result.stdout}\n"
            if result.stderr:
                output += f"STDERR: {result.stderr}\n"
        return output.strip()
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Arguments to pass to the Python file",
            ),
        },
    ),
)