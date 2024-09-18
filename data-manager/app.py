import os

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from classes.data import bazaar_data
from classes.verify_data import verify_bazaar_data
from classes.time import get_current_time
from file_upload import FileUploadManager

# TODO: Pass onto data to other services
# Also allow for usage of enviroment variables

# Initalise file upload manager
fileUploader = FileUploadManager(os.environ.get('FILE_SERVER'))

# Starlette functions

async def recieve_bazaar_data(request):
    request_data = await request.json()
    
    if verify_bazaar_data(request_data):
        number_of_products = len(request_data.get('products', []).keys())
        print(f"Recieved valid bazaar data\nLast Updated: {request_data.get('lastUpdated', None)}\nNumber of products: {number_of_products}")
        
        try:
            fileUploader.uploadFile(f"bazaar/rawData/{(get_current_time())}.json", request_data)
        except Exception as e:
            print(f"Failed to upload file: {e}")
        
        return JSONResponse({'status': 'success', 'message': 'Recieved valid bazaar data'})
    
routes = [
    Route('/healthcheck', lambda request: JSONResponse({'status': 'success', 'message': 'Healthy'})),
    Route('/bazaar', recieve_bazaar_data, methods=['POST'])
]

app = Starlette(routes=routes)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=80)