import os

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        
        dir_content = os.listdir(full_path)
        if directory == ".":
            directory_word = "current"
        else: directory_word = directory
        dir_contents_str = f"Result for {directory_word} directory\n"
        for content in dir_content:
            fuller_path = os.path.join(full_path, content)
            dir_contents_str += f" - {content}: file_size={os.path.getsize(fuller_path)} is_dir={os.path.isdir(fuller_path)}\n"
    except Exception as e:
        return "Error:" + str(e)
    
    return dir_contents_str.rstrip("\n")

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(full_path, 'r', encoding='utf-8') as file:
            content = file.read(10001)
            if len(content) > 10000:
                content = content[:-1]
                content += f"[...File {file_path} truncated at 10000 characters]"
        
        return content
    except Exception as e:
        return "Error:" + str(e)

    