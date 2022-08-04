from django.shortcuts import render
from .models import Event
from .forms import EventForm
# Create your views here.

def home(request):
    events = Event.objects.all()
    context = {"events":events}
    return render(request, "base/home.html", context)

def event(request, pk):
    event = Event.objects.get(id=pk)    
    context = {"event": event}
    return render(request, "base/event.html", context)

def createEvent(request):
    form = EventForm()
    context = {"form":form}
    return render(request, "base/event_form.html", context)

def updateEvent(request, pk):
    context = {}
    return render(request, "base/event_form.html", context)