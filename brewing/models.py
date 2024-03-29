import json
from django.db import models

# Create your models here.
class recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)
    bier_sorte = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    ausschlagwuerze = models.CharField(max_length=100, default="")
    sudhausausbeute = models.CharField(max_length=100)
    stamwuerze = models.CharField(max_length=100)
    ibu = models.IntegerField()
    ebc = models.IntegerField()
    alcohol = models.FloatField(default=0)
    description = models.TextField(max_length=1000)
    brauwasser = models.CharField(max_length=800)
    schuettung = models.CharField(max_length=800)
    maischplan = models.CharField(max_length=800)
    wuerzekochen = models.CharField(max_length=800)
    gaerung = models.CharField(max_length=800)
    phase = models.CharField(max_length=8000)
    
    def __str__(self):
        return f"{self.name}: {self.bier_sorte}"
    

class brew_recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)
    bier_sorte = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    ausschlagwuerze = models.CharField(max_length=100, default="")
    sudhausausbeute = models.CharField(max_length=100)
    stamwuerze = models.CharField(max_length=100)
    ibu = models.IntegerField()
    ebc = models.IntegerField()
    alcohol = models.FloatField(default=0)
    description = models.TextField(max_length=1000)
    brauwasser = models.CharField(max_length=800)
    schuettung = models.CharField(max_length=800)
    maischplan = models.CharField(max_length=800)
    wuerzekochen = models.CharField(max_length=800)
    gaerung = models.CharField(max_length=800)
    phase = models.CharField(max_length=8000)
    number_of_brews = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.name}: {self.description}"
    
    def getRecipe(self):
        return {
            "name": self.name,
            "brauwasser":   json.dumps(self.brauwasser),
            "schuettung":   json.dumps(self.schuettung),
            "wuerzekochen": json.dumps(self.wuerzekochen),
            "phase":        json.dumps(self.phase),
            "command":      "recipe"
        }

class messurement(models.Model):
    time = models.DateTimeField(auto_now=True)
    temperature = models.CharField(max_length=10)
    plato = models.CharField(max_length=10)
    engine = models.BooleanField(default=False)
    step = models.IntegerField()

    def __str__(self):
        return f"{self.time}: {self.temperature}"