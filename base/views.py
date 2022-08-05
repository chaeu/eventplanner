from django.shortcuts import render, redirect
from .models import Event
from .forms import EventForm
# Create your views here.

def home(request):
    nextevent = Event.objects.exclude(eventdate=None).first()
    events = Event.objects.all().exclude(eventdate=None)[1:]
    eventsnodate = Event.objects.all().filter(eventdate=None)
    context = {
        "events":events,
        "nextevent":nextevent,
        "nodate":eventsnodate,    
    }
    return render(request, "base/home.html", context)

def event(request, pk):
    event = Event.objects.get(id=pk)    
    context = {"event": event}
    return render(request, "base/event.html", context)

def createEvent(request):
    form = EventForm()
    
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        print(request.POST)

    context = {"form":form}
    return render(request, "base/event_form.html", context)

def updateEvent(request, pk):
    event = Event.objects.get(id=pk)
    form = EventForm(instance=event)

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form":form}
    return render(request, "base/event_form.html", context)



def deleteEvent(request, pk):
    event = Event.objects.get(id=pk)
    if request.method == "POST":
        event.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj":event})