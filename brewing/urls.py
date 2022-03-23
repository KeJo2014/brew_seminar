from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("evaluate", views.evaluate, name="evaluate"),
    path("home", views.home, name="home"),
    path("delete/<int:recipe_id>", views.delete, name="delete"),
    path("brewing/<int:recipe_id>", views.brewing, name="brewing"),
    path("create", views.create, name="create"),
    path("edit/<int:recipe_id>", views.edit, name="edit"),
    path("template", views.template, name="template"),
]