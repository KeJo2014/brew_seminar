import json
import os

class process_logger():
    def __init__(self):
        self.file = 'brewing/process/logs/proccess_log.json'

    def read(self):
        with open(self.file, 'r') as f:
            return(json.load(f))

    def save(self, data):
        os.remove(self.file)
        with open(self.file, 'w') as f:
            json.dump(data, f, indent=4)


    def new(self):
        self.save({})

    def insert(self, header, insert_data):
        data = self.read()
        data[header] = insert_data
        self.save(data)