import websockets
import asyncio

async def client():
    async with websockets.connect("ws://localhost:8080") as websocket:
        await websocket.send(input())
        response = await websocket.recv()
        print("Server:", response)

asyncio.run(client())