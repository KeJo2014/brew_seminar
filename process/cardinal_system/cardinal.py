from asyncio.windows_events import NULL
import json
from logging import error


errorList = NULL


def load_errorlist():
    """
    load cardinalsystem errors
    """
    global errorList
    data = open("process\cardinal_system\errorList.cardinal", "r")
    errorList = json.loads(data.readline())['error_codes']


def check_command(command, current_processes, recipe):
    """
    checks if the command is allowed
    """
    print(
        f"current progress: {current_processes['recipe-progress']+1} | Server state: {current_processes['Server-Status']}")
    global errorList
    if(command == "start" or command == "select_recipe"):
        if(current_processes["Server-Status"] == "passive"):
            return('granted')
        else:
            return(errorList["405a"])
    if(command == "select_recipe" or command == "reset"):
        if(current_processes["Server-Status"] != "passive"):
            return('granted')
        else:
            return(errorList["405b"])
    elif(command == "next"):
        if(current_processes["recipe-progress"] < len(recipe['roadmap']['points'])):
            if(current_processes["Server-Status"] != "passive"):
                return('granted')
            else:
                return(errorList["405b"])
        else:
            return(errorList['403a'])
    elif(command == "stop"):
        return('granted')
    elif(command == "undo_last" or command == "switch_to_maischen"):
        if(current_processes["Server-Status"] != "passive"):
            if(current_processes["recipe-progress"] > 0):
                return('granted')
            else:
                return(errorList['403b'])
        else:
            return(errorList['405b'])
    else:
        print(command)
        return(errorList['500'])
