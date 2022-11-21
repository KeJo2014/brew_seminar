import random
import os

class brew_server_hardware():
    def __init__(self):
        self.engine = False
        self.heat = False

    def get_temp(self):
        return(random.randint(0,100))


    def heat_on(self):
        print("heating...")
        self.heat = True
        os.system("echo Hello from the other side!")
    
    def heat_off(self):
        self.heat = False
        os.system("echo Hello from the other side!")

    def get_engine_mode(self):
        return self.engine
    
    def get_heat_mode(self):
        return self.heat

    def engine_on(self):
        self.engine = True
        print("engine mode set to: True")
        os.system("echo Hello from the other side!")
    
    def engine_off(self):
        self.engine = False
        print("engine mode set to: False")
        os.system("echo Hello from the other side!")
    
    def get_sensor_object(self):
        ## temp, engine, heating
        return([self.get_temp(), self.get_engine_mode(), self.get_heat_mode()])