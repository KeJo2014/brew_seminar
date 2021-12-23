import json

def interpretRecipe(path):
    data = open(path,"r")
    return(json.loads(data.readline()))