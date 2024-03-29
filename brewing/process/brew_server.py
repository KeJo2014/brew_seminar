import json
from linecache import cache
import time
import logging
import asyncio
from .hardware import brew_server_hardware
from .process_logging import process_logger

from ..models import brew_recipe, messurement
from django.shortcuts import get_object_or_404


class brew_server():    # Übergabe this (Consumer)
    def __init__(self):
        self.eye_of_agamotto = 60    # time 1 = time in seconds || 60 = time in minutes
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
            "brewing_up_time": current_time
        }
        self.roadmap = [[
            "Geräte überprüfen",
            "Materialien überprüfen",
            "Maischen",
            "Läutern",
            "Würzekochen",
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
        self.proccess_logger = process_logger()
        self.logger = logging.getLogger()
        self.handler = logging.FileHandler('brewing/process/logs/logfile.log')
        self.logger.addHandler(self.handler)
        self.last_phase = 0

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
        if(self.status["status"] == "maischen"):
            s["phases"] = self.load_phases(0)
        elif(self.status["status"] == "Würzekochen" or self.status["status"] == "warmingUp" or self.status["status"] == "cooking"):
            s["phases"] = self.load_phases(1)
        return s

    def write_to_log(self, message):
        timeStr = time.ctime()
        self.logger.error(timeStr+": " + message)

    def load_recipe(self, recipe_id):
        rec = json.dumps(brew_recipe.objects.get(id=recipe_id).recipe)
        self.status["recipe"] = rec
        self.recipe = json.loads(brew_recipe.objects.get(id=recipe_id).recipe)

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

    def next_step(self, consumer):
        print(f'new step: {self.roadmap[0][self.status["step"]+1]}')
        if(self.recipe != None):
            if(self.status["step"] != len(self.roadmap[0])-1):
                if(self.roadmap[0][self.status["step"]+1] == "Maischen"):
                    self.initiate_maischen(consumer)
                    self.status["step"] -= 1
                elif(self.roadmap[0][self.status["step"]+1] == "Würzekochen"):
                    self.initiate_kochen(consumer)
                    self.status["step"] -= 1
                self.status["step"] += 1
                return(True)
            else:
                return(False)

    def manual_engine(self, data):
        if(data == "on"):
            self.hardware.engine_on()
        else:
            self.hardware.engine_off()

    def maischen_procedure(self, consumer):
        print(f'DAUER: {self.maischen["end"]-time.time()}')
        if(time.time() > self.maischen["end"]):
            print("finish")
            self.proccess_logger.insert(f'FieldID_ABMAISCHEN_ZEIT', time.time())
            self.status["status"] = "running"
            self.hardware.engine_off()
            self.status["sensor_data"]["engine_mode"] = False
            self.next_step(consumer)
        else:
            self.status["status"] = "maischen"
            # DB get phases
            print(self.get_recipe())
            phases = self.load_phases(0)
            # print(phases)

            # get current phase
            delta = time.time() - self.maischen["start"]
            for i in range(len(phases)):
                if(delta/self.eye_of_agamotto < phases[i][1]):
                    if(self.last_phase != i+1):
                        self.proccess_logger.insert(f'FieldID_RAST_{i+2}', time.time())
                        self.last_phase = i+1
                    heating_duration = self.heat(
                        phases[i][0], consumer)     # returns heating time
                    self.maischen["end"] = self.maischen["end"] + heating_duration
                    print(
                        f'adding {heating_duration}: new end time: {self.maischen["end"]}')
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

    def kochen_procedure(self, consumer):
        print("COOKING")
        if(time.time() > self.kochen["end"]):
            print("finish")
            self.proccess_logger.insert(f'FieldID_KOCHEN_END_ZEIT', time.time())
            self.status["status"] = "running"
            self.next_step(consumer)
        else:
            self.status["status"] = "cooking"
            root = self.load_phases(1)
            phases = root[1]
            # print(f'HERE {phases}')
            # get current phase
            delta = time.time() - self.kochen["start"]
            for i in range(len(phases)):
                if(delta/self.eye_of_agamotto < (int(root[0]) - int(phases[i][3]))):
                    if(self.last_phase != i):
                        self.proccess_logger.insert(f'FieldID_KOCHEN_{i+1}HOPFEN', time.time())
                        self.last_phase = i
                    heating_duration = self.heat(95, consumer)            # QUESTION 5
                    self.kochen["end"] = self.kochen["end"] + heating_duration
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

    # step 0 = maischen, step 1 = würzekochen
    def load_phases(self, step):
        recipe = brew_recipe.objects.get(id=self.status["recipe"])
        if(step == 0):
            print(recipe.maischplan)
            temp = json.loads(recipe.maischplan)[0][2]
            print(temp)
            phases = []
            cache = 0
            for i in range(len(temp)):
                phases.append([int(temp[i][0]), int(temp[i][1])+cache])
                cache += int(temp[i][1])
        else:
            temp = json.loads(recipe.wuerzekochen)
            print(temp)
            phases = []
            phases.append(temp[0])
            temp2 = []
            for i in range(len(temp)):
                if(i != 0):
                    temp2.append(
                        [temp[i][0], temp[i][1], temp[i][2], temp[i][3]])
            phases.append(temp2)

        return phases

    def keep_process(self, consumer):
        print(self.roadmap[0][self.status["step"]])
        if(self.roadmap[0][self.status["step"]] == "Maischen"):
            self.maischen_procedure(consumer)
        elif(self.roadmap[0][self.status["step"]] == "cooking" or self.roadmap[0][self.status["step"]] == "Würzekochen"):
            self.kochen_procedure(consumer)

    def initiate_maischen(self, consumer):
        phases = self.load_phases(0)
        duration = phases[len(phases)-1][1]
        self.status["step"] += 1
        print(self.heat(int(json.loads(brew_recipe.objects.get(
            id=self.status["recipe"]).maischplan)[0][1]), consumer))
        self.maischen = {
            "start": time.time(),
            "end": time.time()+(duration*self.eye_of_agamotto)
        }
        print(self.maischen["end"])
        self.status["status"] = "maischen"
        self.status["start_time"] = time.time()
        self.proccess_logger.insert(f'FieldID_RAST_1', time.time())
        self.hardware.engine_on()

    def initiate_kochen(self, consumer):
        print("INITIATE")
        phases = self.load_phases(1)
        # print(phases)
        duration = int(phases[0])
        print("initiate kochen")
        self.status["step"] += 1
        self.heat(int(95), consumer)              # QUESTION TEMP
        self.kochen = {
            "start": time.time(),
            "end": time.time()+(duration*self.eye_of_agamotto)
        }
        print(self.kochen["end"])
        self.status["status"] = "warmingUp"
        self.status["start_time"] = time.time()
        self.proccess_logger.insert(f'FieldID_KOCHEN_START_ZEIT', time.time())
        print("ENDE")

    def heat(self, destination_temp, consumer):
        if(consumer != ""):
            heat = self.hardware.get_heat_mode()
            #heat = False
            start_time = time.time()
            while(self.hardware.get_temp() < destination_temp):
                if(heat is False):
                    self.hardware.heat_on()
                    heat = True                           #-> send Update data
                print(f'temp: {self.hardware.get_temp()}')
                print(f'send {json.dumps(self.get_status())}')
                # consumer.send_json(
                #     {'type': 'chat_message', 'message': json.dumps(self.get_status())})
                consumer.send(text_data=json.dumps({
                    'type': 'chat_message',
                    'message': json.dumps({"message":self.get_status()})
                }))
                time.sleep(2)
            self.hardware.heat_off()
            return (time.time()-start_time)
        else:
            heat = self.hardware.get_heat_mode()
            # heat = False
            start_time = time.time()
            while(self.hardware.get_temp() < destination_temp):
                if(heat is False):
                    self.hardware.heat_on()
                    heat = True                           #-> send Update data
                print(f'temp: {self.hardware.get_temp()}')
                time.sleep(2)
                self.hardware.heat_off()
            return (time.time()-start_time)

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
        self.proccess_logger.new()
        self.proccess_logger.insert("FieldID_DATUM", time.time())
        return(True)

    def getProtocolData(self):
        return {"command": "getProcessData", "data": self.proccess_logger.read()}

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
            "Würzekochen",
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