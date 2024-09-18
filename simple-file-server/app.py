from json import JSONDecodeError

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse, FileResponse

from functions.file_functions import *

import os
import uvicorn

DOCKER_CONTAINER = os.environ.get('DOCKER_CONTAINER')

if DOCKER_CONTAINER:
    BASE_DIR = '/files'
else:
    BASE_DIR = "SET_YOUR_BASE_DIR_HERE"
    
# Route functions

# TODO: Add permissions to routes (using API keys) to allow for creation of directories, deletion of files, etc.
# Also assign different permissions to different API keys, which allows each service to access different files / directories
# And prevents certain services from deleting / creating files etc.

# LATER: Also allow for access to an SQL database, which will allow for easier data management and querying
# This will speed up the process of finding files, and allow for more complex queries to be run on the data
# Might archive this repository and create a new one for the SQL database, as it will be a vastly different project

# Starlette routes

async def get_files(request):
    directory = BASE_DIR
    
    files = list_files(directory)
    if not files:
        return JSONResponse({'error': 'Directory not found'}, status_code=404)
    
    return JSONResponse(files)

async def get_file(request):
    filename = request.path_params['filename']
    file_path = os.path.join(BASE_DIR, filename)
    
    file = download_file(file_path)
    
    if file.get('error'):
        return JSONResponse(file, status_code=404)
    
    return FileResponse(file)

async def send_file(request):
    # TODO: Add permissions to this route, and error handling
    print("Received a file upload request")
    form = await request.form()

    files_written = await upload_file(form, BASE_DIR)

    response = JSONResponse({'success': True, 'files_written': files_written}) 
    return response

async def delete_file(request):
    filenames = request.query_params.getlist('filenames')
    
    removed_files = remove_file(BASE_DIR, filenames)
    
    if 'error' in removed_files:
        return JSONResponse(removed_files, status_code=400)
    
    return JSONResponse(removed_files)

routes = [
    Route('/', get_files, methods=['GET']),
    Route('/{filename}', get_file, methods=['GET']),
    Route('/', send_file, methods=['POST']),
    Route('/', delete_file, methods=['DELETE'])
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=80)