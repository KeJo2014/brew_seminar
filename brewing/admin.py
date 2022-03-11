from django.contrib import admin

from .models import recipe, messurement
# Register your models here.

class data_points(admin.ModelAdmin):
    list_display = ("time", "temperature", "plato", "step")

admin.site.register(recipe)
admin.site.register(messurement, data_points)