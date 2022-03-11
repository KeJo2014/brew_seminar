import json
import time
from datetime import datetime
import logging

from ..models import recipe

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
            },
            "start_time": current_time,
        }
        self.logger = logging.getLogger()
        self.handler = logging.FileHandler('brewing/process/logs/logfile.log')
        self.logger.addHandler(self.handler)
    
    def get_status(self):
        return self.status
    
    def write_to_log(self, message):
        timeStr = time.ctime()
        self.logger.error(timeStr+": " +message)
    
    def load_recipe(self, recipe_id):
        rec  = json.dumps(recipe.objects.get(id=recipe_id).recipe)
        self.status["recipe"] = rec
