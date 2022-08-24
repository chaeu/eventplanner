from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import Event, Topic, Message
from .forms import EventForm



# Create your views here.

def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password is incorrect")

    context = {
        "page":page
    }
    return render(request, "base/login_register.html", context)

def logoutUser(request):
    logout(request)
    return redirect("home")

def registerPage(request):
    #page = "register"
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occured during registration, pleasy try again.")
    return render(request, "base/login_register.html", {"form":form})

def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""    
    events = Event.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(description__icontains=q)     
        )
    
    upcoming_events = events.filter(eventdate__gt=timezone.now()) 
    past_events = events.filter(eventdate__lt=timezone.now())
    
    nextevent = upcoming_events.exclude(eventdate=None).first()
    #upcoming_events = upcoming_events[1:]
    #events = Event.objects.all().exclude(eventdate=None)
    #eventsnodate = Event.objects.all().filter(eventdate=None)

    topics = Topic.objects.all()
    event_count = events.count()
    event_messages = Message.objects.all().filter(Q(event__topic__name__icontains=q))

    if request.method == "POST" and "join" in request.POST:
        event = Event.objects.get(id=int(request.POST["join"]))
        if event.eventdate > timezone.now():
            event.participants.add(request.user)
            return redirect(reverse("home") + "?q="+ q)
    elif request.method == "POST" and "leave" in request.POST:   
        event = Event.objects.get(id=int(request.POST["leave"]))        
        if event.eventdate > timezone.now():
            event.participants.remove(request.user)
            return redirect(reverse("home") + "?q="+q)

    context = {
        "events":events,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "topics": topics,
        "event_count":event_count,
        "event_messages": event_messages,
        "nextevent":nextevent,
        #"nodate":eventsnodate,            
    }
    return render(request, "base/home.html", context)

def event(request, pk):
    event = Event.objects.get(id=pk)    
    event_messages = event.message_set.all()
    participants = event.participants.all()
    capacity = event.capacity

    if request.method =="POST":
        """message = Message.objects.create(
            user=request.user,
            event=event,
            body=request.POST.get("body")
        )"""
        event.participants.add(request.user)
        return redirect("event", pk=event.id)
    
    context = {
        "event": event, 
        "event_messages": event_messages,
        "participants": participants,      
        "capacity": capacity,  
        }
    return render(request, "base/event.html", context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    events = user.event_set.all()
    event_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        "user": user, 
        "events": events, 
        "event_messages": event_messages,
        "topics": topics,
        }
    return render(request, "base/profile.html", context)

@login_required(login_url="login")
def createEvent(request):    
    form = EventForm()
    
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            #event.host = request.user
            event.save()
            return redirect("home")
        print(request.POST)

    context = {"form":form}
    return render(request, "base/event_form.html", context)

@login_required(login_url="login")
def updateEvent(request, pk):
    event = Event.objects.get(id=pk)
    form = EventForm(instance=event)

    if request.user != event.host:
        return HttpResponse("You are not allowed to do that")

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form":form}
    return render(request, "base/event_form.html", context)

@login_required(login_url="login")
def deleteEvent(request, pk):
    event = Event.objects.get(id=pk)

    if request.user != event.host:
        return HttpResponse("You are not allowed to do that")

    if request.method == "POST":
        event.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj":event})

@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not allowed to do that")

    if request.method == "POST":
        message.delete()        
        return redirect("home")

    return render(request, "base/delete.html", {"obj": message})