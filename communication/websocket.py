import asyncio
import websockets

connected = set()


async def server(websocket, path):
    # Register.
    connected.add(websocket)
    print(f'{websocket} connected')
    try:
        async for message in websocket:
            print(f'{message} received')
            for conn in connected:
                await conn.send(f'Got a new MSG FOR YOU: {message}')
                # if conn != websocket:                                      # Send to everyone except the sender.
                #    await conn.send(f'Got a new MSG FOR YOU: {message}')
    finally:
        # Unregister.
        connected.remove(websocket)
        print(f'{websocket} disconnected')
