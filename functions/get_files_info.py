import os

from google.genai import types

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_path, directory))
        if  not os.path.commonpath([working_path, target_dir]) == working_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        files = []
        direct = "current" if directory == "." else directory
        result = f"Result for {direct} directory:"
        #print(f"Result for {direct} directory:")
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            is_dir = False
            if os.path.isdir(item_path):
                is_dir = True
            result += f"\n    - {item}: file_size={os.path.getsize(item_path)}, is_dir={is_dir}"
            #print(f"    - {item}: file_size={os.path.getsize(item_path)}, is_dir={is_dir}")
        return result
    except Exception as e:
        return f'Error: {e}'


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)