from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("evaluate", views.evaluate, name="evaluate"),
    path("home", views.home, name="home"),
    path("brewing", views.brewing, name="brewing"),
    path("create", views.create, name="create"),
    path("template", views.template, name="template"),
]