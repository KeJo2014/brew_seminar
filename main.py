import asyncio
from asyncio.windows_events import NULL
import json
import logging
import websockets
import os


from process.communication.websocket import *
from process.brauablauf import interpretRecipe
from process.db import create_new_table, insert_into_table
from process.trigger.funk import getTemperature, getMotorMode
from process.timer import *

recipe = []
current_processes = []

logging.basicConfig()


def check_turn_pages():
    global recipe
    global current_processes

    for i in range(len(recipe['roadmap']['points'])):
        if(recipe['roadmap']['points'][i] == "Maischen"):
            if(i == current_processes['recipe-progress']):
                return(True)
    return(False)


async def maischen():
    global recipe
    print(recipe['recipe'])
    create_new_table()
    time = 0
    designations = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth", "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth", "seventeenth", "eighteenth",
                    "nineteenth", "twentieth", "twenty-first", "twenty-second", "twenty-third", "twenty-fourth", "twenty-fifth", "twenty-sixth", "twenty-seventh", "twenty-eighth", "twenty-ninth", "thirtieth", "thirty-first"]
    for i in range(len(recipe['recipe']['data']['maischplan'])):
        time += recipe['recipe']['data']['maischplan']['rests'][designations[i]]['duration']

    set_timer(time, recipe)
    todo = f"heating up to {recipe['recipe']['data']['maischplan']['Einmaischen']} degrees celcius..."
    await send_maisch_update(getTemperature(), getMotorMode(), minute, todo)
    await heat_to(recipe['recipe']['data']['maischplan']['Einmaischen'])
    start_timer()
    # if USERS:  # asyncio.wait doesn't accept an empty list
    #    await asyncio.wait([user.send() for user in USERS])


async def maischen_procedure():

    if USERS:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([user.send("procedure") for user in USERS])


async def server(websocket, path):
    # register(websocket) sends user_event() to websocket
    global default
    global recipe
    global sources_path
    global current_processes

    await register(websocket)
    try:
        await websocket.send(json.dumps(default))
        async for message in websocket:
            data = json.loads(message)
            if(data["command"] == "start"):
                await start_brewing(recipe)
            elif(data["command"] == "next"):
                current_processes = await next_step(current_processes)
                if(check_turn_pages()):

                    await switch_to_maischen()
            elif(data["command"] == "select_recipe"):
                npath = sources_path+"/recipes/"+data["response"]
                recipe = interpretRecipe(npath)
                await send_response(json.dumps(recipe))
            elif(data["command"] == "reset"):
                current_processes = await reset(recipe, current_processes)
            elif(data["command"] == "undo_last"):
                current_processes = await undo_last(current_processes)
            elif(data["command"] == "stop"):
                current_processes = await stop(current_processes)
            elif(data["command"] == "switch_to_maischen"):
                await maischen()
            else:
                logging.error("unsupported event: %s", data["command"])
    finally:
        await unregister(websocket)

 ########################################################################## main part ##########################################################################
# loading global variables
# read recipe
sources_path = "./sources"
recipe = {"error": "no recipe selected"}
logging.info("recipe successfully loaded!")

# setting default tasks
default = {
    "Server-Status": "passive",
    "recipe-progress": 0
}
current_processes = default
start_server = websockets.serve(server, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
