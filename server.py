import uvicorn
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
from typing import Dict
import websockets

app = FastAPI()

connections: Dict[str, WebSocket] = {}


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    connections[user_id] = websocket
    print(f"Connected user {user_id}")
    print(f"Current connections: {connections}")
    try:
        while True:
            data = await websocket.receive_json()
            print(f"Received data: {data}")
            recipient = data['recipient']
            message = data['message']
            print(recipient, message)
            await send_message(recipient, message)
    except WebSocketDisconnect:
        del connections[user_id]
        print(f"Disconnected user {user_id}")
        print(f"Current connections: {connections}")


async def send_message(recipient: str, message: str):
    print(connections)
    if recipient in connections:
        print(recipient)
        websocket = connections[recipient]
        await websocket.send_json({"sender": "server", "message": message})


# @app.post("/send_message/{user_id}")
# async def send_message_view(user_id: str, message: str):
#     await send_message(user_id, message)
#     return {"message": "Message sent"}


# async def receive_messages(user_id: str):
#     print(f"Current connections: {connections}")
#     print(f"Receiving messages for user {user_id}")
#     if user_id in connections:
#         websocket = connections[user_id]
#         while True:
#             message = await websocket.receive_text()
#             print(f"Received message for user {user_id}: {message}")


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)

    print('PyCharm')

