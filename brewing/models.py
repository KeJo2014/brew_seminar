from django.db import models

# Create your models here.
class recipe(models.Model):
    last_brewed = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    recipe = models.CharField(max_length=5000)
    
    def __str__(self):
        return f"{self.name}: {self.recipe}"

class messurement(models.Model):
    time = models.DateTimeField(auto_now=True)
    temperature = models.CharField(max_length=10)
    plato = models.CharField(max_length=10)
    engine = models.BooleanField(default=False)
    step = models.IntegerField()

    def __str__(self):
        return f"{self.time}: {self.temperature}"