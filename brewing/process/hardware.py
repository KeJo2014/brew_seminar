import os
import time
import random


class brew_server_hardware():
    def __init__(self):
        self.engine = False
        self.heat = False

    def get_temp(self):
        try:
            tempfile = open("/sys/bus/w1/devices/28-00000d5d9de2/w1_slave")
            inhalt = tempfile.read()
            tempfile.close()
            tempdata = inhalt.split("\n")[1].split(" ")[9]
            temperatur = float(tempdata[2:])
            temperatur = temperatur/1000
            return (temperatur)
        except:
            print("ACHTUNG: SENSOR DEFEKT")
            return (random.randint(0,110))

    def heat_on(self):
        #os.system("brewing/process/RPi_utils/codesend 1397077")
        print("heating...")
        self.heat = True

    def heat_off(self):
        #os.system("brewing/process/RPi_utils/codesend 1397076")
        self.heat = False

    def get_engine_mode(self):
        return self.engine

    def get_heat_mode(self):
        return self.heat

    def engine_on(self):
        self.engine = True
        #os.system("brewing/process/RPi_utils/codesend 1381717")
        print("engine mode set to: True")

    def engine_off(self):
        self.engine = False
        #os.system("brewing/process/RPi_utils/codesend 1381716")
        print("engine mode set to: False")

    def get_sensor_object(self):
        # temp, engine, heating
        return ([self.get_temp(), self.get_engine_mode(), self.get_heat_mode()])
