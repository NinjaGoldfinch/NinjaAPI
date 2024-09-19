import websockets
import asyncio
import json

class WebsocketHandler:
    def __init__(self, uri: str, data_queue: list) -> None:
        self.ws_uri = "ws://" + uri
        self.data_queue = data_queue
        self.service_name = 'bazaar-updater'
    
    def dict_to_json(self, data: dict) -> str:
        return json.dumps(data)
    
    def simplify_data(self, data: dict):
        print("Sent data to websocket server!")
        return {'lastUpdated': data.get('lastUpdated', None), 'products': len(data.get('products', {}).keys())}
    
    async def send_config(self, websocket: websockets.WebSocketClientProtocol):
        config = self.dict_to_json({'service_type': self.service_name})
        await websocket.send(config)
        print(f"Sent configuration: {config}")
        print("Waiting for response...")
        
        response = await websocket.recv()
        print(f"Recieved response: {response}")

    async def send_data(self, websocket: websockets.WebSocketClientProtocol, data: dict):
        display_data = self.simplify_data(data)
        data = self.dict_to_json(data)
        await websocket.send(data)
        print(f"Sent data: {display_data}")
        print("Waiting for response...")
        
        response = await websocket.recv()
        print(f"Recieved response: {response}")
    
    async def start_websocket(self):
        print("Starting websocket connection...")
        try:
            async with websockets.connect(self.ws_uri) as websocket:
                await self.send_config(websocket)
                while True:
                    if len(self.data_queue) > 0:
                        data = self.data_queue.pop(0)
                        await self.send_data(websocket, data)
                    else:
                        await asyncio.sleep(0.1)
        except ConnectionRefusedError:
            print("Failed to connect to websocket server. Retrying in 1 second...")
            await asyncio.sleep(1)
            await self.start_websocket()