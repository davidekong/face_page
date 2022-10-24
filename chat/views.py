from multiprocessing import context
from urllib import response
from django.shortcuts import redirect, render
import schedule
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from chat.models import Room

# Create your views here.



            

def lobby(request):
    if request.method == "POST":
        room = Room.objects.get(room_name=request.POST['room_name'])
        if room != None:
            return redirect('room', pk=room.id)
    return render(request, 'chat/lobby.html')



def room(request, pk):
    context = {
        'room_name': Room.objects.get(pk=pk).room_name, 
        'id': str(pk)
    }
    room = Room.objects.get(room_name=context['room_name'])

    
    
    return render(request, 'chat/room.html', context)

