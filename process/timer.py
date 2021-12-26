import asyncio
from asyncio.windows_events import NULL
from process.communication.websocket import send_finish_maisch, send_maisch_update
from process.trigger.funk import get_temperature, get_motor_mode, heat_to, hold_current_temperature, engine
from process.db import insert_into_table

timer = 0
task = NULL
minute = 0
current_step = 0

recipe = NULL
last_time = 0


def set_timer(time, rec):
    """
    sets the timer to the given time and loads the recipe
    """
    print(f'set timer: {time}')
    global timer
    global recipe
    recipe = rec
    timer = time


async def procedure():
    """
    starts every minute and leads through the 'maischen' procedure
    """
    global minute
    global current_step
    global last_time
    while True:
        print(f'Minute: {minute}')
        minute += 1
        designations = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth", "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth", "seventeenth", "eighteenth",
                        "nineteenth", "twentieth", "twenty-first", "twenty-second", "twenty-third", "twenty-fourth", "twenty-fifth", "twenty-sixth", "twenty-seventh", "twenty-eighth", "twenty-ninth", "thirtieth", "thirty-first"]
        todo = ""
        if(minute == recipe['recipe']['data']['maischplan']['rests'][designations[current_step]]['duration']+last_time):
            if(current_step < len(recipe['recipe']['data']['maischplan']['rests'])-1):
                last_time += recipe['recipe']['data']['maischplan']['rests'][designations[current_step]]['duration']
                current_step += 1
                print(f'current step: {current_step}')
                todo = f"heating up for step Nr. {current_step}"
                print(
                    f"current step: {current_step} || length: {len(recipe['recipe']['data']['maischplan']['rests'])}")
                if(current_step >= len(recipe['recipe']['data']['maischplan']['rests'])-1):
                    print('finished!')
                    todo = "maischen finished"
                    engine(False)
                    await send_finish_maisch()
                    stop()
                else:
                    await heat_to(recipe['recipe']['data']['maischplan']['rests'][designations[current_step]]['temperature'])
            else:
                print('finished!')
                engine(False)
                todo = "maischen finished"
                await send_finish_maisch()
                stop()
        else:
            print("holding temperature")
            await hold_current_temperature(recipe['recipe']['data']['maischplan']['rests'][designations[current_step]]['temperature'])
            todo = f"holding temperature (~{recipe['recipe']['data']['maischplan']['rests'][designations[current_step]]['temperature']} Grad) -{current_step}"
        insert_into_table(get_temperature(), get_motor_mode())
        await send_maisch_update(get_temperature(), get_motor_mode(), minute, todo)
        await asyncio.sleep(0.1)


def stop():
    """
    stops the procedure
    """
    global task
    task.cancel()
    reset()


def reset():
    """
    resets the timer
    """
    global timer
    global last_time
    global current_step
    global minute
    minute = 0
    timer = 0
    current_step = 0
    last_time = 0
    print('reseted')


def start_timer():
    """
    starts the maischen procedure
    """
    global task
    global timer
    global recipe
    global last_time
    engine(True)
    last_time = 0
    timer = 71
    print(f'start: duration: {timer} minutes')
    loop2 = asyncio.get_event_loop()
    loop2.call_later(timer, stop)
    task = loop2.create_task(procedure())
