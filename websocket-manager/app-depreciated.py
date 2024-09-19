import asyncio
import uvicorn

from starlette.applications import Starlette
from starlette.routing import WebSocketRoute
from starlette.websockets import WebSocket

# Custom variables

bazaar_service = 'disconnected'

# Websocket functions
async def recieve_config(websocket: WebSocket):
    print("Waiting for configuration data...")
    config = await websocket.receive_json()
    print("Recieved configuration data:", config)
    
    return config

async def process_config(config: dict):
    print(config)
    if config.get('service_type', None) == 'ninja/bazaar-updater':
        print("Internal server type: Ninja/Bazaar Updater. Enabling bazaar websocket...")
        return {'name': 'bazaar-updater', 'service_type': 'ninja/bazaar-updater'}
    else:
        print("Connection isn't an internal service.")
        return {'name': 'unknown', 'service_type': 'listener'}

async def recieve_bazaar_data(websocket: WebSocket):
    print("Waiting for bazaar data...")
    data = await websocket.receive_json()
    print("Recieved bazaar data:", data)
    
    return data

async def send_json_response(websocket: WebSocket, data: dict):
    await websocket.send_json(data)
    print("Sent json message:", data)

# Websocket server routes
async def websocket_route(websocket: WebSocket):
    await websocket.accept()
    
    config_data = await recieve_config(websocket)
    config_settings = await process_config(config_data)
    
    client_name = config_settings.get('name', 'unknown')

    if client_name == 'bazaar-updater':
        bazaar_service = 'connected'
        print("Bazaar service connected.")
        await send_json_response(websocket, {'status': 'success', 'message': 'Recieved configuration data. Listening for Bazaar data.'})
    else:
        print("Unknown service connected.")
        await send_json_response(websocket, {'status': 'success', 'message': 'Connection established. Waiting for new data'})
                
    while True:
        if client_name == 'ninja/bazaar-updater':
            data = await recieve_bazaar_data(websocket)
            print("Recieved data:", data)
            
            websocket.send_json({'status': 'success', 'message': 'Recieved new Bazaar data.'})
    
# Start the data and websocket servers

ws_routes = [
    WebSocketRoute('/', websocket_route)
]

def run_ws_app():
    ws_app = Starlette(routes=ws_routes)
    uvicorn.run(ws_app, host='0.0.0.0', port=80)

if __name__ == "__main__":
    run_ws_app()