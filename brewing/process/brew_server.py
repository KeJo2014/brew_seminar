import json
from pickle import FALSE
import time
from datetime import datetime
import logging

from ..models import recipe, messurement

class brew_server():
    def __init__(self):
        current_time = time.time()
        self.status ={
            "status": "started",
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
            "Läutern",
            "Kochen",
            "Gären",
        ],[
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
        return s
    
    def write_to_log(self, message):
        timeStr = time.ctime()
        self.logger.error(timeStr+": " +message)
    
    def load_recipe(self, recipe_id):
        rec  = json.dumps(recipe.objects.get(id=recipe_id).recipe)
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
       messurement.objects.create(self.status["sensor_data"]["temperature"], self.status["sensor_data"]["engine_mode"], self.status["sensor_data"]["plato"])
    
    def next_step(self):
        if(self.recipe != None):
            if(self.status["step"] != len(self.roadmap[0])-1):
                self.status["step"] += 1
                return(True)
            else:
                return(False)

    def step_back(self):
        if(self.status["step"] != 0):
            self.status["step"] -= 1
            return(True) 
        else:
            return(False)
    
    def start_process(self):
        print("start process")
        return(True)
    
    def stop_process(self):
        current_time = time.time()
        self.status ={
            "status": "started",
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
            "Läutern",
            "Kochen",
            "Gären",
        ],[
            "You haven't createt a field to track notes ;-)",
            "You haven't createt a field to track notes ;-)",
            "You haven't createt a field to track notes ;-)",
            "You haven't createt a field to track notes ;-)",
            "You haven't createt a field to track notes ;-)",
        ]]
        self.recipe = []
        return(True)