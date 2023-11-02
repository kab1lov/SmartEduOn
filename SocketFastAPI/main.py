import base64

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect

app = FastAPI()

app.mount("/static", StaticFiles(directory="/app/Frontend/static"), name="static")


class WebSocketManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def send_to_all(self, data: str):
        for connection in self.active_connections:
            await connection.send_text(data)


manager = WebSocketManager()


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_to_all(data)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)


@app.post('/sendfile')
async def send_file(file_data: bytes):
    base64_data = base64.b64encode(file_data).decode('utf-8')
    await manager.broadcast(base64_data)
    return {'message': 'File sent'}
