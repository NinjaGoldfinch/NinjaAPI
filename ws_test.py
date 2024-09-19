import websockets
import asyncio
import json

DEBUG = False

async def send_config(websocket: websockets.WebSocketClientProtocol, serviceName: str):
    config = {'service_type': serviceName}
    await websocket.send(json.dumps(config))
    
    response = await websocket.recv()
    if DEBUG:
        print(f"Recieved response: {response}")


async def recieve_data(websocket: websockets.WebSocketClientProtocol):
    if DEBUG:
        print("Recieving data...")
    data = await websocket.recv()
    
    return data

async def get_data(websocket: websockets.WebSocketClientProtocol, message: json.dumps):
    await websocket.send(message)
    if DEBUG:
        print("Sent data request.")
    
    response = await recieve_data(websocket)
    if DEBUG:
        print(f"Recieved data: {response}")
    return response
    
async def startWebsocket():
    uri = "ws://localhost:8080"
    async with websockets.connect(uri, max_size=None) as websocket:
        await send_config(websocket, 'abc')
        print("Connected to websocket server. Recieving data...")
        while True:
            response = await get_data(websocket, json.dumps({'request': 'bazaar_data'}))
            
            bazaar_data = json.loads(response)
            
            if bazaar_data.get('status', None) == 'success':
                print("Recieved bazaar data:", bazaar_data.get('data', None))
            
if __name__ == "__main__":
    asyncio.run(startWebsocket())