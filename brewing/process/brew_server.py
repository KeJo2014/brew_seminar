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
            "recipe": 0,
            "step": 0,
            "sensor_data": {
                "temperature": 0,
                "engine_mode": False,
                "plato": 0,
            },
            "start_time": current_time,
        }
        self.recipe = []
        self.logger = logging.getLogger()
        self.handler = logging.FileHandler('brewing/process/logs/logfile.log')
        self.logger.addHandler(self.handler)
    
    def get_status(self):
        s = self.status
        s["command"] = "update"
        return s
    
    def write_to_log(self, message):
        timeStr = time.ctime()
        self.logger.error(timeStr+": " +message)
    
    def load_recipe(self, recipe_id):
        rec  = json.dumps(recipe.objects.get(id=recipe_id).recipe)
        self.status["recipe"] = rec
        self.recipe = json.loads(recipe.objects.get(id=recipe_id).recipe)
    
    def write_sensor_data(self):
       messurement.objects.create(self.status["sensor_data"]["temperature"], self.status["sensor_data"]["engine_mode"], self.status["sensor_data"]["plato"])
    
    def next_step(self):
        if(self.recipe != 0):
            if(self.status["step"] != len(self.recipe["roadmap"]["points"])):
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