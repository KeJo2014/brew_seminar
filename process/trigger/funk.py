import random
import asyncio

motor_mode = False

def engine(mode):
    global motor_mode
    if mode == True:
        print("Motor on")
        motor_mode = True
        #sending to power
    else:
        print("Motor off")
        motor_mode = False
        #sending to power

def get_temperature():
    return(random.randint(0,100))

def get_motor_mode():
    return(motor_mode)

async def heat_to(degrees):
    while(get_temperature() < degrees):
        print('heater Fon')

async def hold_current_temperature(degrees):
    if(get_temperature() <= degrees-2):
        print('heater on')
    else:
        print('heater off')