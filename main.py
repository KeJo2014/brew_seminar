import asyncio
from asyncio.windows_events import NULL
import json
import logging
import os
import websockets
import process.cardinal_system.cardinal as cardinal


from process.communication.websocket import beginn_brewing, send_maisch_update, register, next_step, send_boiling_update, send_error, switch_to_maischen, reset, stop, undo_last, send_response, unregister, USERS
from process.brauablauf import interpretRecipe
from process.db import create_new_table
from process.trigger.funk import engine, get_temperature, get_motor_mode, heat_to
from process.timer import set_timer, start_timer, get_boiling_point_at_position
from process.data_protocol.manage_protocol import save_protocol


recipe = []
current_processes = []

logging.basicConfig()


def check_turn_pages():
    """
    checks if client needs to switch to maischen
    """
    global recipe
    global current_processes
    for i in range(len(recipe['roadmap']['points'])):
        if(recipe['roadmap']['points'][i] == "Maischen" and i == current_processes['recipe-progress']):
            return('maischen')
        elif(recipe['roadmap']['points'][i] == "Kochen" and i == current_processes['recipe-progress']):
            return('würzekochen')
    return('nope')


async def maischen():
    """
    starts the maischen procedure
    """
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
    await send_maisch_update(get_temperature(), get_motor_mode(), 0, todo)
    await heat_to(recipe['recipe']['data']['maischplan']['Einmaischen'])
    start_timer(current_processes['recipe-progress'])


async def switch_to_wuerzekochen():
    """
    switches to würzekochen
    """
    global recipe
    print(recipe['recipe'])
    time = 0
    designations = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth", "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth", "seventeenth", "eighteenth",
                    "nineteenth", "twentieth", "twenty-first", "twenty-second", "twenty-third", "twenty-fourth", "twenty-fifth", "twenty-sixth", "twenty-seventh", "twenty-eighth", "twenty-ninth", "thirtieth", "thirty-first"]
    for i in range(len(recipe['recipe']['wÃ¼rzekochen']['hop'])):
        time = recipe['recipe']['wÃ¼rzekochen']['hop'][designations[i]]['time']
    set_timer(time, recipe)
    todo = f"heating up to {recipe['recipe']['wÃ¼rzekochen']['hop'][designations[i]]['time']} degrees celcius..."
    await send_boiling_update(get_temperature(), 0, todo)
    await heat_to(get_boiling_point_at_position())
    start_timer(current_processes['recipe-progress'])


async def server(websocket, path):
    """
    starts the websocket server
    """
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
            if(cardinal.check_command(data["command"], current_processes, recipe) == "granted"):
                if(data["command"] == "start"):
                    default = {"Server-Status": "up and running",
                               "recipe-progress": 0}
                    current_processes = default
                    await beginn_brewing(recipe)
                elif(data["command"] == "next"):
                    current_processes = await next_step(current_processes)
                    if(check_turn_pages() == "maischen"):
                        await switch_to_maischen()
                    elif(check_turn_pages() == "würzekochen"):
                        await switch_to_wuerzekochen()
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
                    exit()
                elif(data["command"] == "switch_to_maischen"):
                    await maischen()
                elif(data["command"] == "safe_protocol"):
                    save_protocol(data['protocol'])
                else:
                    logging.error("unsupported event: %s", data["command"])
            else:
                await send_error(cardinal.check_command(data["command"], current_processes, recipe))
    finally:
        await unregister(websocket)

 ########################################################################## main part ##########################################################################
# loading global variables
# read recipe

os.chdir('../Brauanlage/brew_seminar')
sources_path = "./sources"
recipe = {"error": "no recipe selected"}
logging.info("recipe successfully loaded!")

# setting default tasks
engine(False)
cardinal.load_errorlist()
default = {
    "Server-Status": "passive",
    "recipe-progress": 0
}
current_processes = default
start_server = websockets.serve(server, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
