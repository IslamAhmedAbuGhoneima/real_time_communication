from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import User
from account.forms import EditUserForm
from .models import Room
import json
# Create your views here.

@require_POST
def create_room(request, uuid):
    data = json.loads(request.body)
    name = data['name']
    url = data['url']
    Room.objects.create(
        uuid=uuid,
        client=name,
        url=url
    )
    return JsonResponse({'message': 'room created'})


@login_required
def admin(request):
    rooms = Room.objects.all()
    users = User.objects.filter(is_staff=True)
    return render(request, 'chat_app/admin.html', {"rooms": rooms, "users": users})


@login_required
def room(request, uuid):
    room = Room.objects.get(uuid=uuid)
    if room.status == Room.CHOICES_STATUS[0][0]:
        room.status = Room.CHOICES_STATUS[1][0]
        room.agent = request.user
        room.save()
    return render(request, 'chat_app/room.html', {'room': room})


@login_required
def delete_room(request, uuid):
    if request.user.has_perm("room.delete_room"):
        try:
            room = Room.objects.get(uuid=uuid)
            room.delete()
            messages.success(request, 'room deleted successfuly')
            return redirect('chat_app:admin')
        except:
            raise ValueError(Room.DoesNotExist)
    else:
        messages.error(request, 'You dont\'t have access to delete this room')
        return redirect('chat_app:admin')


@login_required
def user_detail(request, uuid):
    user = User.objects.prefetch_related("rooms").get(id=uuid)
    rooms = user.rooms.all()
    return render(request, 'chat_app/user_detail.html', {'user': user, "rooms": rooms})


def edit_user(request, uuid):
    user = User.objects.get(id=uuid)
    form = EditUserForm(instance=user)
    if request.user.has_perm('user.edit_user'):
        if request.method == "POST":
            form = EditUserForm(data=request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Changes saved successfully')
                return redirect('chat_app:admin')
    else:
        messages.error(request, 'Error happen when update user')
    return render(request, 'chat_app/edit_user.html', {"form": form})
