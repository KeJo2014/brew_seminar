import json
import time
import logging
import asyncio
from .hardware import brew_server_hardware

from ..models import recipe, messurement


class brew_server():
    def __init__(self):
        current_time = time.time()
        self.hardware = brew_server_hardware()
        self.status = {
            "status": "waiting",
            "recipe": None,
            "step": 0,
            "sensor_data": {
                "temperature": 0,
                "engine_mode": False,
                "heat_mode": False,
                "plato": 0,
            },
            "start_time": current_time,
        }
        self.roadmap = [[
            "Geräte überprüfen",
            "Materialien überprüfen",
            "Maischen",
            "Läutern",
            "Kochen",
            "Gären",
        ], [
            "You haven't createt a field to track notes ;-)",
            "You haven't createt a field to track notes ;-)",
            "You haven't createt a field to track notes ;-)",
            "You haven't createt a field to track notes ;-)",
            "You haven't createt a field to track notes ;-)",
            "You haven't createt a field to track notes ;-)",
        ]]
        self.recipe = []
        self.logger = logging.getLogger()
        self.handler = logging.FileHandler('brewing/process/logs/logfile.log')
        self.logger.addHandler(self.handler)

    def get_status(self):
        s = self.status
        s["command"] = "update"
        s["roadmap"] = self.roadmap
        x = {
            "temperature": self.hardware.get_temp(),
            "engine_mode": self.hardware.get_engine_mode(),
            "heat_mode": self.hardware.get_heat_mode(),
            "plato": self.status["sensor_data"]["plato"]
        }
        s["sensor_data"] = x
        return s

    def write_to_log(self, message):
        timeStr = time.ctime()
        self.logger.error(timeStr+": " + message)

    def load_recipe(self, recipe_id):
        rec = json.dumps(recipe.objects.get(id=recipe_id).recipe)
        self.status["recipe"] = rec
        self.recipe = json.loads(recipe.objects.get(id=recipe_id).recipe)

    def get_recipe(self):
        if(self.status["recipe"] != None):
            return(self.status["recipe"])
        else:
            return(None)

    def set_recipe(self, recipe_id):
        self.status["recipe"] = recipe_id

    def write_sensor_data(self):
        data = messurement(temperature=self.status["sensor_data"]["temperature"], plato=self.status["sensor_data"]
                           ["plato"], engine=self.status["sensor_data"]["engine_mode"], step=self.status["step"])
        data.save()

    def next_step(self):
        if(self.recipe != None):
            if(self.status["step"] != len(self.roadmap[0])-1):
                if(self.roadmap[0][self.status["step"]+1] == "Maischen"):
                    self.initiate_maischen()
                self.status["step"] += 1
                return(True)
            else:
                return(False)

    def maischen_procedure(self):
        if(time.time() > self.maischen["end"]):
            print("finish")
            self.status["status"] = "running"
            self.hardware.engine_off()
            self.status["sensor_data"]["engine_mode"] = False
            self.next_step()
        else:
            # DB get phases
            phases = [
                [20, 50],
                [35, 55],
                [75, 64],
                [95, 72],
                [115, 78]
            ]
            # get current phase
            delta = time.time() - self.maischen["start"]
            for i in range(len(phases)):
                if(delta > phases[i][0] and delta < phases[i][1]):
                    self.heat(phases[i][0])
                    break

            obj = self.hardware.get_sensor_object()
            print("here")
            self.status["sensor_data"] = {
                "temperature": obj[0],
                "engine_mode": obj[1],
                "heat_mode": obj[2],
                "plato": self.status["sensor_data"]["plato"]
            }
            self.write_sensor_data()
            time.sleep(3)

    def initiate_maischen(self):
        self.maischen = {
            "start": time.time(),
            "end": time.time()+20
        }
        self.status["status"] = "warmingUp"
        self.hardware.engine_on()

    def heat(self, destination_temp):
        while(self.hardware.get_temp() < destination_temp):
            self.hardware.heat_on()
            time.sleep(1)
        self.hardware.heat_off()

    def step_back(self):
        if(self.status["step"] != 0):
            if(self.roadmap[0][self.status["step"]-1] == "Maischen"):
                self.initiate_maischen()
            self.status["step"] -= 1
            return(True)
        else:
            return(False)

    def start_process(self):
        print("start process")
        self.status["status"] = "running"
        return(True)

    def stop_process(self):
        current_time = time.time()
        self.status = {
            "status": "waiting",
            "recipe": None,
            "step": 0,
            "sensor_data": {
                "temperature": 0,
                "engine_mode": False,
                "plato": 0,
            },
            "start_time": current_time,
        }
        self.roadmap = [[
            "Geräte überprüfen",
            "Materialien überprüfen",
            "Maischen",
            "Läutern",
            "Kochen",
            "Gären",
        ], [
            "You haven't createt a field to track notes ;-)",
            "You haven't createt a field to track notes ;-)",
            "You haven't createt a field to track notes ;-)",
            "You haven't createt a field to track notes ;-)",
            "You haven't createt a field to track notes ;-)",
            "You haven't createt a field to track notes ;-)",
        ]]
        self.recipe = []
        return(True)
