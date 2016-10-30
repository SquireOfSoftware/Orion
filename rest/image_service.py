from django.http import HttpResponse
from django.utils import timezone
import json
from rest.models import Image
from rest.models import Mission


def get_current_time():
    time = timezone.now().__str__()
    return time


def get_current_image():
    return send_response(Image.objects.last().as_dict())


def get_images(start_number, end_number):
    pass


def post_images(image_object, mission_id):
    try:
        Image.objects.create(imagetimestamp=get_current_time(),
                             imageblob=image_object,
                             mission_missionid=Mission.objects.get(missionid=mission_id))
        return send_response({"status": "True"})
    except Mission.DoesNotExist:
        return send_image_error("Mission does not exist")


def send_response(message):
    return HttpResponse(json.dumps(message))


def send_image_error(message):
    return HttpResponse(json.dumps({"status": "error",
                                    "data": message
                                    }),
                        status=403)