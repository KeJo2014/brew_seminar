import random
import asyncio

motor_mode = False

def motor(mode):
    global motor_mode
    if mode == True:
        print("Motor on")
        motor_mode = True
        #sending to power
    else:
        print("Motor off")
        motor_mode = False
        #sending to power

def getTemperature():
    return(random.randint(0,100))

def getMotorMode():
    return(motor_mode)

async def heat_to(degrees):
    while(getTemperature() < degrees):
        print('heater Fon')

async def hold_current_temperature(degrees):
    if(getTemperature() <= degrees-2):
        print('heater on')
    else:
        print('heater off')