import asyncio
import uvicorn

from starlette.applications import Starlette
from starlette.routing import WebSocketRoute
from starlette.websockets import WebSocket, WebSocketDisconnect

# Custom variables

bazaar_service = 'disconnected'
data_to_send = {'bazaar': [], 'auction': []}


# Websocket functions
async def recieve_config(websocket: WebSocket):
    print("Waiting for configuration data...")
    config = await websocket.receive_json()
    print("Recieved configuration data:", config)
    
    return config

async def process_config(config: dict):
    print(config)
    if config.get('service_type', None) == 'bazaar-updater':
        print("Internal server type: Ninja/Bazaar Updater. Enabling bazaar websocket...")
        return {'name': 'bazaar-updater', 'service_type': 'ninja/bazaar-updater'}
    else:
        print("Connection isn't an internal service.")
        return {'name': 'unknown', 'service_type': 'listener'}


# Websocket server routes
async def websocket_route(websocket: WebSocket):
    await websocket.accept()
    
    config_data = await recieve_config(websocket)
    config_settings = await process_config(config_data)
    
    client_name = config_settings.get('name', 'unknown')
    client_ready = 0
    
    if client_name == 'bazaar-updater':
        bazaar_service = 'connected'
        print("Bazaar service connected.")
        await websocket.send_json({'status': 'success', 'message': 'Recieved configuration data. Listening for Bazaar data.'})
    else:
        print("Unknown service connected.")
        await websocket.send_json({'status': 'success', 'message': 'Listening for new data.'})
    
    try:
        while True:          
            if client_name == 'bazaar-updater':
                print("Waiting for new data.")
                data = await websocket.receive_json()
                data_to_send['bazaar'].append(data)
                print(f"Recieved bazaar data: {len(data.get('products', {}).keys())} products detected.")
                await websocket.send_json({'status': 'success', 'message': 'Recieved data'})

            elif client_name == 'unknown':
                response = await websocket.receive_json()
                if response.get('request', False) == 'bazaar_data':
                    if len(data_to_send['bazaar']) > 0:
                        data = {'status': 'success', 'data': data_to_send['bazaar'].pop(0), 'remaining': len(data_to_send)}
                        await websocket.send_json(data)
                    else:
                        await websocket.send_json({'status': 'error', 'message': 'No data to send.'})
                          
    except WebSocketDisconnect:
        print("Client disconnected.")
        if client_name == 'bazaar-updater':
            bazaar_service = 'disconnected'
    except Exception as e:
        print(f"Error: {e}")
        print("Closing websocket connection...")

# Start the data and websocket servers

ws_routes = [
    WebSocketRoute('/', websocket_route)
]

def run_ws_app():
    ws_app = Starlette(routes=ws_routes)
    uvicorn.run(ws_app, host='0.0.0.0', port=80)

if __name__ == "__main__":
    run_ws_app()