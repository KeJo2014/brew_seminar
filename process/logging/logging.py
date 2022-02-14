import json

class Logger:
    def __init__(self, start_d, start_t):
        self.log_file = open("process.log", "a")
        self.log_file.write('helo?!')
        print("Logger started")
        self.log_file.close()

    def log_change_step(self, step):
        self.log_file = open("process.log", "r")
        self.content = json.loads(self.log_file.read())
        self.content["current_step"] = step
        self.log_file = open("process.log", "x")
        self.log_file.write(json.dumps(self.content))
    
    def get_logs(self):
        self.log_file = open("process.log", "r")
        self.content = self.log_file.read()
        self.log_file.close()
        return '{"meta":{"start_date":"01.06.22","start_time":"15:00","current_step":3,"recipe_name":"Test"}}'

