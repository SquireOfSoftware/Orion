from django.http import HttpResponse
import json

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


def get_images(start_number, end_number):
    return HttpResponse(json.dumps({"start": start_number, "end": end_number}))