from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("event/<str:pk>/", views.event, name="event"), 
    path("create-event/", views.createEvent, name="create-event"),
    path("update-event/", views.updateEvent, name="update-event")
]