import asyncio
import os
import uvicorn
import threading

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from classes.verify_data import verify_bazaar_data
from classes.time import get_current_time
from file_upload import FileUploadManager
from ws_handler import WebsocketHandler

# TODO: Pass onto data to other services
# Also allow for usage of enviroment variables

# Initalise file upload manager
fileUploader = FileUploadManager(os.environ.get('FILE_SERVER'))
websocket_uri = os.environ.get('WEBSOCKET_SERVER')

data_queue = []

# Functions

def ws_handler(uri: str, data_queue: list):
    ws = WebsocketHandler(uri, data_queue)
    asyncio.run(ws.start_websocket())

async def send_data(data, fileUploader):
    fileUploader.uploadFile(f"bazaar/rawData/{(get_current_time())}.json", data)
    data_queue.append(data)

# Starlette functions

async def recieve_bazaar_data(request):
    request_data = await request.json()
    
    if verify_bazaar_data(request_data):
        number_of_products = len(request_data.get('products', []).keys())
        print(f"Recieved valid bazaar data\nLast Updated: {request_data.get('lastUpdated', None)}\nNumber of products: {number_of_products}")
        
        await send_data(request_data, fileUploader)
        
        return JSONResponse({'status': 'success', 'message': 'Recieved valid bazaar data'})

routes = [
    Route('/bazaar', recieve_bazaar_data, methods=['POST'])
]

app = Starlette(routes=routes)

if __name__ == '__main__':
    ws_thread = threading.Thread(target=ws_handler, daemon=True, args=(websocket_uri, data_queue))
    ws_thread.start()
    uvicorn.run(app, host='0.0.0.0', port=80)
    ws_thread.join()