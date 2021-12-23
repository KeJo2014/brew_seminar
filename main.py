import asyncio
from asyncio.windows_events import NULL
import json
import logging
import websockets

from process.brauablauf import interpretRecipe

protocol = []
currentProcesses = []

logging.basicConfig()

STATE = {"value": 0}

USERS = set()


def state_event():
    return json.dumps({"type": "state", **STATE})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def start_brewing():
    global currentProcesses
    global protocol
    default = {
        "Server-Status": "up and running",
        "recipe-progress": 0
    }
    currentProcesses = default

    if USERS:  # asyncio.wait doesn't accept an empty list
        message = json.dumps(protocol)
        await asyncio.wait([user.send(message) for user in USERS])


async def next_step():
    global currentProcesses
    default = {
        "Server-Status": "up and running",
        "recipe-progress": currentProcesses["recipe-progress"] + 1
    }
    currentProcesses = default

    if USERS:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([user.send(json.dumps(currentProcesses)) for user in USERS])


async def send_error(message):
    if USERS:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([user.send(message) for user in USERS])


async def undo_last():
    global currentProcesses
    default = {
        "Server-Status": "up and running",
        "recipe-progress": currentProcesses["recipe-progress"] - 1
    }
    currentProcesses = default

    if USERS:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([user.send(json.dumps(currentProcesses)) for user in USERS])


async def reset():
    global currentProcesses
    global protocol
    default = {
        "Server-Status": "up and running",
        "recipe-progress": 0
    }
    currentProcesses = default

    if USERS:  # asyncio.wait doesn't accept an empty list
        message = json.dumps(protocol)
        await asyncio.wait([user.send(message) for user in USERS])
        await asyncio.wait([user.send(json.dumps(currentProcesses)) for user in USERS])


async def stop():
    global currentProcesses
    default = {
        "Server-Status": "passive",
        "recipe-progress": 0
    }
    currentProcesses = default

    if USERS:  # asyncio.wait doesn't accept an empty list
        logging.error("SERVER IS STOPPED")
        await asyncio.wait([user.send(json.dumps(currentProcesses)) for user in USERS])


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


async def server(websocket, path):
    # register(websocket) sends user_event() to websocket
    global default

    await register(websocket)
    try:
        await websocket.send(json.dumps(default))
        async for message in websocket:
            data = json.loads(message)
            if(data["command"] == "start"):
                await start_brewing()
            elif(data["command"] == "next"):
                await next_step()
            elif(data["command"] == "reset"):
                await reset()
            elif(data["command"] == "undo_last"):
                await undo_last()
            elif(data["command"] == "stop"):
                await stop()
            else:
                logging.error("unsupported event: %s", data["command"])
    finally:
        await unregister(websocket)

 ########################################################################## main part ##########################################################################
# loading global variables
# read protocol
path = r"C:\Users\Jonas\Documents\Brauanlage\brew_seminar\sources\recipes\test.fbp"
protocol = interpretRecipe(path)
logging.info("recipe successfully loaded!")

# setting default tasks
default = {
    "Server-Status": "passive",
    "recipe-progress": 0
}
currentProcesses.append(default)
start_server = websockets.serve(server, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
