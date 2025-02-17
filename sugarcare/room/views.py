from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Message
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def index(request):
    allowed_users=['johndoe', 'sugarcare']
    if request.user.username not in allowed_users:
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    rooms = Room.objects.all()
    return render(request, 'rooms.html', {'rooms': rooms})


def room(request, room_name):
    room = get_object_or_404(Room, slug=room_name)
    messages = Message.objects.filter(room=room)
    return render(request, 'room.html', {'room': room, 'messages': messages,})


def create_room(request):
    room_name= request.user.username
    room_slug= room_name

    room, created= Room.objects.get_or_create(
        slug=room_slug,
        defaults={'name':f"{room_name}"}
    )
    return redirect('room', room_name= room_slug)


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        print(request.POST)  # Log POST data
        room_name = request.POST.get('room')
        room = get_object_or_404(Room, slug=room_name)
        message_text = request.POST.get('message', '')
        image = request.FILES.get('image', None)

        message = Message.objects.create(
            room=room,
            user=request.user,
            content=message_text,
            image=image
        )

        # Send the message to the WebSocket
        response_data = {
            'username': request.user.username,
            'message': message.content,
            'image': message.image.url if message.image else None,
        }

        return JsonResponse(response_data)
