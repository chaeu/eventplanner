from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("event/<str:pk>/", views.event, name="event"), 
    path("create-event/", views.createEvent, name="create-event"),
    path("update-event/<str:pk>/", views.updateEvent, name="update-event"),
    path("delete-event/<str:pk>/", views.deleteEvent, name="delete-event"),
]