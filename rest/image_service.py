from django.http import HttpResponse
import json
from rest.models import Image


images_taken = [
    {
        "id": 1,
        "mission_id": 1,
        "path": "static/images/12345.jpeg"
     },
    {
        "id": 2,
        "mission_id": 1,
        "path": "static/images/12346.jpeg"
    }
]


def get_current_image():
    return send_response(Image.objects.last().as_dict())


def get_images(start_number, end_number):
    pass


def send_response(message):
    return HttpResponse(json.dumps(message))