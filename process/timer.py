import asyncio
from process.maischen import send_status
from asyncio.windows_events import NULL
from process.communication.websocket import send_finish_maisch, send_maisch_update
from process.trigger.funk import getTemperature, getMotorMode, heat_to, hold_current_temperature
from process.db import insert_into_table


timer = 0
task = NULL
minute = 0
current_step = 0

recipe = NULL

def set_timer(time,rec):
    print(f'set timer: {time}')
    global timer
    global recipe
    recipe = rec
    timer = time

async def procedure():
    global minute
    global current_step
    while True:
        print(f'Minute: {minute}')
        minute += 1
        designations = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth", "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth", "seventeenth", "eighteenth", "nineteenth", "twentieth", "twenty-first", "twenty-second", "twenty-third", "twenty-fourth", "twenty-fifth", "twenty-sixth", "twenty-seventh", "twenty-eighth", "twenty-ninth", "thirtieth", "thirty-first"]
        if(minute == recipe['recipe']['data']['maischplan']['rests'][designations[current_step]]['duration']-1):
            if(current_step < len(recipe['recipe']['data']['maischplan']['rests'])-1):
                current_step += 1
                print(f'current step: {current_step}')
                await heat_to(recipe['recipe']['data']['maischplan']['rests'][designations[current_step]]['temperature'])
            else:
                print('finished!')
                await send_finish_maisch()
        else:
            await hold_current_temperature(recipe['recipe']['data']['maischplan']['rests'][designations[current_step]]['temperature'])
            
        
        todo = "nothing"

        insert_into_table(getTemperature(), getMotorMode())
        await send_maisch_update(getTemperature(), getMotorMode(), minute, todo)
        await asyncio.sleep(1)

def stop():
    global task
    task.cancel()

def start_timer():
    global task
    global timer
    print(f'start: duration: {timer} minutes')
    loop2 = asyncio.get_event_loop()
    loop2.call_later(timer, stop)
    task = loop2.create_task(procedure())

    
