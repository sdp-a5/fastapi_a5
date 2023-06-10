import os
import uvicorn
from typing import List
from fastapi import FastAPI, UploadFile, status, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from util import remove_directories, create_directory, save_file
import util
import worker
import time


uploadpath = os.getcwd() + "/uploads/"
archivepath = os.getcwd() + "/archive/"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload/{username}", status_code=status.HTTP_201_CREATED)
async def create_files(sample_image: UploadFile, group_images: List[UploadFile], username: str) -> FileResponse:

    # creating directories
    create_directory(uploadpath + username + "/sample")
    create_directory(uploadpath + username + "/group")
    create_directory(uploadpath + username + "/extracted")
    create_directory(uploadpath + username + "/compare")
    create_directory(uploadpath + username + "/facial_folder")
    create_directory(uploadpath + username + "/result")
    create_directory(archivepath + username)

    # saving sample photo
    sample_image_name = F"sample.{sample_image.filename.split('.')[-1]}"
    save_file(F"{uploadpath}{username}/sample/{sample_image_name}", sample_image)

    # saving group photos
    for image in group_images:
        filename = image.filename
        print(filename)
        save_file(F"{uploadpath}{username}/group/{filename}", image)
    
    abc =  os.path.join('/uploads',username)

    result_path=worker.findcomapre(abc)

    print(result_path)

    if len(os.listdir(result_path)) > 0:
        print('matches are there')
    
    else:
        print('matches not found')

    # Example usage
    folder_path = result_path
    output_path = os.path.join(archivepath + username + '/result.zip')

    print(output_path)

    util.zip_folder(folder_path, output_path)

    # removing temporary files from the upload and out directory
    remove_directories(uploadpath + username)

    
    response = FileResponse(path=archivepath+username+"/result.zip")
    response.headers["content-disposition"] = f'attachment; filename="{username}.zip"'
    response.headers["Content-Type"] = "application/octet-stream"
    return response


@app.get("/cleanup/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def cleanup(username: str) -> None:
    remove_directories(archivepath+username+"/")


@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exception: Exception):
    if request.url.path.startswith("/upload/"):
        username: str = request.path_params.get("username")
        remove_directories(archivepath+username+"/")
    return JSONResponse({"error": ["Exception occured", str(exception)]}, status_code=500)


# if __name__ == "__main__":
#     uvicorn.run(app="main:app", port=8000, host="localhost", reload=True)
