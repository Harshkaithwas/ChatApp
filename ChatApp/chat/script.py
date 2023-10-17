import asyncio
import websockets
import json

async def send_and_receive():
    async with websockets.connect("ws://127.0.0.1:8000/ws/chat/harshi/") as websocket:
        # Send a message to the WebSocket server
        await websocket.send(json.dumps({'message': 'Hello, WebSocket!'}))

        # Receive messages from the WebSocket server
        async for message in websocket:
            print(f"Received: {message}")

asyncio.get_event_loop().run_until_complete(send_and_receive())
