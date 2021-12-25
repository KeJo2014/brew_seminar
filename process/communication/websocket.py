import asyncio
import json
import logging

STATE = {"value": 0}

USERS = set()


def state_event():
    """
    loads events
    """
    return('{command:"response"}')


def users_event():
    """
    load number of connected clients
    """
    return json.dumps({"type": "users", "count": len(USERS)})


def all_recipes():
    """
    sends the list of all recipes
    """
    # on Linux: x = os.listdir("./sources/recipes")
    logging.info("loading all recipes...")
    # on Linux: return json.dumps(x)
    return('{"Server":{"Server-Status":"passive","recipe-progress":0},"recipes":["test.fbp","notThat.fbp"],"command":"select_recipe"}')


async def notify_state():
    """
    sends the state event
    """
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def beginn_brewing(recipe):
    """
    send the beginn brewing command to client
    """
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = json.dumps(recipe)
        await asyncio.wait([user.send(message) for user in USERS])


async def next_step(current_processes):
    """
    get the next step of the recipe
    """
    default = {
        "Server-Status": "up and running",
        "recipe-progress": (current_processes['recipe-progress'] + 1)
    }
    current_processes = default

    if USERS:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([user.send(json.dumps(current_processes)) for user in USERS])
    return(current_processes)


async def send_error(message):
    """
    sends an error message to the client
    """
    if USERS:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([user.send(message) for user in USERS])


async def send_finish_maisch():
    """
    sends the finish maisch command to client
    """
    if USERS:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([user.send('{"command":"finish_maisch"}') for user in USERS])


async def send_maisch_update(temp, motor, current_time, todo):
    """
    updates current stats
    """
    if USERS:  # asyncio.wait doesn't accept an empty list
        cpu_temp = 12  # get real value
        message = json.dumps({"command": "m_update", "m_temp": temp, "engine_mode": motor,
                             "cpu_temp": cpu_temp, "time": current_time, "todo": todo})
        print(message)
        await asyncio.wait([user.send(message) for user in USERS])


async def undo_last(current_processes):
    """
    go one step back in recipe
    """
    default = {
        "Server-Status": "up and running",
        "recipe-progress": (current_processes["recipe-progress"] - 1)
    }
    current_processes = default

    if USERS:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([user.send(json.dumps(current_processes)) for user in USERS])
    return(current_processes)


async def switch_to_maischen():
    """
    starts maischen command
    """
    if USERS:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([user.send('{"command": "switch_to_maischen"}') for user in USERS])


async def reset(recipe, current_processes):
    """
    restes current process in the selected recipe
    """
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
    """
    send server stop command
    """
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
    """
    notify all users about the number of connected clients
    """
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = all_recipes()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    """
    register a new connected client
    """
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    """
    unregister a disconnected client
    """
    USERS.remove(websocket)
    await notify_users()


async def send_response(response):
    """
    sends a response to the client
    """
    if USERS:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([user.send(response) for user in USERS])
