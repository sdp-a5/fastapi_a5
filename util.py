import os
import shutil
import zipfile
from typing import List
from fastapi import UploadFile


def remove_directories(directory: str) -> None:
    try:
        shutil.rmtree(directory)
    except OSError as e:
        print(e)


def save_file(file_name_with_location: str, file_stream: UploadFile) -> None:
    with open(file_name_with_location, "wb") as file:
        content = file_stream.file.read()
        file.write(content)


def create_directory(directory_path: str) -> None:
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def create_response_zip(zip_path: str, list_of_file_locations: List[str]) -> None:
    with zipfile.ZipFile(zip_path+"response.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_location in list_of_file_locations:
            zipf.write(file_location, arcname=os.path.basename(file_location))


def zip_folder(folder_path, output_path):
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return
    
    # Ensure the output path is a .zip file
    if not output_path.endswith('.zip'):
        output_path += '.zip'
    
    # Create a zip file and add all files and subdirectories to it
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=os.path.relpath(file_path, folder_path))
    
    print(f"Folder '{folder_path}' has been zipped to '{output_path}'.")

