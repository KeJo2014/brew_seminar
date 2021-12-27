import asyncio
from asyncio.windows_events import NULL
from process.communication.websocket import send_finish_maisch, send_maisch_update, send_boiling_update, send_finish_boiling
from process.trigger.funk import get_temperature, get_motor_mode, heat_to, hold_current_temperature, engine
from process.db import insert_into_table

timer = 0
task = NULL
minute = 0
current_step = 0

recipe = NULL
last_time = 0
boiling_temp = 0

eye_of_agamotto = 0.1


def set_timer(time, rec):
    """
    sets the timer to the given time and loads the recipe
    """
    print(f'set timer: {time}')
    global timer
    global recipe
    recipe = rec
    timer = time


async def maischen_procedure():
    """
    starts every minute and leads through the 'maischen' procedure
    """
    global minute
    global current_step
    global last_time
    global eye_of_agamotto
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
        insert_into_table(get_temperature(), get_motor_mode(), 'maischen')
        await send_maisch_update(get_temperature(), get_motor_mode(), minute, todo)
        await asyncio.sleep(eye_of_agamotto)


async def boiling_procedure():
    """
    starts every minute and leads through the 'boiling' procedure
    """
    global minute
    global current_step
    global boiling_temp
    global eye_of_agamotto
    while True:
        print(f'Minute: {minute}')
        minute += 1
        designations = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth", "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth", "seventeenth", "eighteenth",
                        "nineteenth", "twentieth", "twenty-first", "twenty-second", "twenty-third", "twenty-fourth", "twenty-fifth", "twenty-sixth", "twenty-seventh", "twenty-eighth", "twenty-ninth", "thirtieth", "thirty-first"]
        todo = ""
        if(minute == recipe['recipe']['wÃ¼rzekochen']['hop'][designations[current_step]]['time']):
            if(minute < recipe['recipe']['wÃ¼rzekochen']['duration']):
                current_step += 1
                print(f'current step: {current_step}')
                todo = f"add following hop"

            else:
                print('finished!')
                todo = "boiling finished"
                await send_finish_boiling()
                stop()
        else:
            print("holding temperature")
            await hold_current_temperature(boiling_temp)
            todo = f"holding temperature (~{boiling_temp} Grad) -{current_step}"
        insert_into_table(get_temperature(), False, 'boiling')
        await send_boiling_update(get_temperature(), minute, todo)
        await asyncio.sleep(eye_of_agamotto)


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


def start_timer(current_step):
    """
    starts the maischen procedure
    """
    global task
    global timer
    global recipe
    global last_time
    engine(True)
    last_time = 0
    print(f'start: duration: {timer} minutes')
    if(recipe['roadmap']['points'][current_step] == 'Maischen'):
        loop2 = asyncio.get_event_loop()
        loop2.call_later(timer, stop)
        task = loop2.create_task(maischen_procedure())
    elif(recipe['roadmap']['points'][current_step] == 'Kochen'):
        loop2 = asyncio.get_event_loop()
        loop2.call_later(timer, stop)
        task = loop2.create_task(boiling_procedure())


def get_boiling_point_at_position():
    """
    returns the boiling point at the current position using van-’t-Hoff’sche Reaktionsisobare
    """
    global boiling_temp
    boiling_temp = 99.46
    return boiling_temp
