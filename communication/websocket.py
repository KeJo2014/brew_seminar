import asyncio
import json
from json.decoder import JSONDecoder
import logging

STATE = {"value": 0}

USERS = set()


def state_event():
    return('{command:"response"}')


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


def all_recipes():
    # on Linux: x = os.listdir("./sources/recipes")
    logging.info("loading all recipes...")
    # on Linux: return json.dumps(x)
    return('{"Server":{"Server-Status":"passive","recipe-progress":0},"recipes":["test.fbp","notThat.fbp"],"command":"select_recipe"}')


async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def start_brewing(recipe):

    if USERS:  # asyncio.wait doesn't accept an empty list
        message = json.dumps(recipe)
        await asyncio.wait([user.send(message) for user in USERS])


async def next_step(current_processes):

    default = {
        "Server-Status": "up and running",
        "recipe-progress": (current_processes['recipe-progress'] + 1)
    }
    current_processes = default

    if USERS:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([user.send(json.dumps(current_processes)) for user in USERS])
    return(current_processes)


async def send_error(message):
    if USERS:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([user.send(message) for user in USERS])


async def undo_last(current_processes):

    default = {
        "Server-Status": "up and running",
        "recipe-progress": (current_processes["recipe-progress"] - 1)
    }
    current_processes = default

    if USERS:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([user.send(json.dumps(current_processes)) for user in USERS])
    return(current_processes)


async def switch_to_maischen():
    if USERS:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([user.send('{"command": "switch_to_maischen"}') for user in USERS])


async def reset(recipe, current_processes):

    default = {
        "Server-Status": "up and running",
        "recipe-progress": 0
    }
    current_processes = default

    if USERS:  # asyncio.wait doesn't accept an empty list
        message = json.dumps(recipe)
        await asyncio.wait([user.send(message) for user in USERS])
        await asyncio.wait([user.send(json.dumps(current_processes)) for user in USERS])
    return(current_processes)


async def stop(current_processes):

    default = {
        "Server-Status": "passive",
        "recipe-progress": 0
    }
    current_processes = default

    if USERS:  # asyncio.wait doesn't accept an empty list
        logging.error("SERVER IS STOPPED")
        await asyncio.wait([user.send(json.dumps(current_processes)) for user in USERS])
    return(current_processes)


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = all_recipes()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


async def send_response(response):
    if USERS:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([user.send(response) for user in USERS])
