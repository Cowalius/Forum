from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm, MessageForm
# Create your views here.

def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")
    if request.method== "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user= User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Wrong data")

    context={"page":page}
    return render(request,'base/login_registration.html', context)

def logOut(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    page = 'register'
    form = UserCreationForm()
    if request.method =="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Something went wrong')

    return render(request, 'base/login_registration.html',{'form':form})


def home(request):
    q = request.GET.get('q', '')  # pobierz wartość parametru q z adresu URL
    if q:
        # pobierz tylko te pokoje, które mają temat odpowiadający wartości q
        rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__contains=q) | Q(description__contains=q))
    else:
        rooms = Room.objects.all()

    # pobierz wszystkie tematy
    topics = Topic.objects.all()

    context = {'rooms': rooms, 'topics': topics}
    return render(request, 'base/home.html', context)


def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('created')
    Users=  room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room':room, "room_messages":room_messages,"Users":Users}
    return render(request, 'base/room.html',context)

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_message=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_message':room_message,'topics':topics}
    return render(request,'base/profile.html', context)

@login_required(login_url="/login/")
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False)
            room.host=request.user
            room.save()
            return redirect('home')
        else:
            return redirect('home')
    context = {'form':form}
    return render(request,"base/room_form.html",context)

@login_required(login_url="/login/")
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse(" You cannot modify this room")

    if request.method=="POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url="/login/")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse(" You cannot delete this room")

    if request.method == "POST":
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse(" You cannot delete this message")

    if request.method == "POST":
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url="login")
def updateMessage(request, pk):
    message = Message.objects.get(id=pk)
    form = MessageForm(instance=message)

    if request.user != message.user:
        return HttpResponse("You cannot modify this message")

    if request.method == "POST":
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/message_form.html', context)


