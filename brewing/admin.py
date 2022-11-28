from django.contrib import admin

from .models import brew_recipe, messurement
# Register your models here.

class data_points(admin.ModelAdmin):
    list_display = ("time", "temperature", "plato", "step")

admin.site.register(brew_recipe)
admin.site.register(messurement, data_points)