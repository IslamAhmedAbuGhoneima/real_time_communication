from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import Room
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
