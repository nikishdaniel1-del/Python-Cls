import websockets
import asyncio

async def handler(websocket):
    async for message in websocket:
        print('received : '+message)
        await websocket.send(input())

async def main():
    async with websockets.serve(handler,host='0.0.0.0',port=8080):
        await asyncio.Future()
asyncio.run(main())