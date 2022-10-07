from email import message
import email
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Room, Message
from django.http import HttpResponse, JsonResponse

# Create your views here.

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "email exist")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username already exist')
                return redirect('login')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save();
                return redirect ('login')
        else:
            messages.info(request, 'password do not match')
            return render(request, 'signup.html')
        
    else:
        return render (request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect ('/')
        else:
            messages.info (request, 'Credentials Do not Match Kindly try again')
            return redirect ('login')
    else:
        return render(request, 'login.html')
def home(request):
    return render (request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render (request, 'room.html', {'username':username, 'room_details': room_details, 'room':room})

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']
    
    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect ('/'+room+'?username='+username)
    
def send (request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    
    new_Message = Message.objects.create(value = message, user = username, room = room_id)
    new_Message.save()
    return HttpResponse ('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)
   # room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room = room_details.id)
    return JsonResponse({"messages":list(messages.values())})

def logout(request):
    auth.logout(request)
    return redirect('login')

