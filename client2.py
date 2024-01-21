import asyncio
import websockets
import json


async def connect_to_websocket(user_id: str):
    async with websockets.connect(f"ws://localhost:8000/ws/{user_id}") as websocket:
        # Send a message to "bob" from a view function
        message = {"recipient": user_id, "message": "Hello, Bob!"}
        await websocket.send(json.dumps(message))

        # Receive messages for "alice"
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(data)
            print(f"Received message from {data['sender']}: {data['message']}")


# Connect to the WebSocket endpoint with user ID "alice"
asyncio.run(connect_to_websocket("bob"))
