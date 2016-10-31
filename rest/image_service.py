from django.http import HttpResponse
from django.utils import timezone
import datetime
from dateutil.parser import parse
import json
from rest.models import Image
from rest.models import Mission


def get_current_time():
    time = timezone.now().__str__()
    return time


def get_current_image():
    return send_response(Image.objects.last().as_dict())


def get_images(start_number, end_number):
    if start_number < end_number:
        image_results = Image.objects.all().order_by("-imagetimestamp")[start_number:end_number]
    else:
        image_results = Image.objects.all()[:10]
    images = [image.as_dict() for image in image_results]
    return send_response(images)


def get_mission_images(mission_id, start_number, end_number):
    try:
        requested_images = Image.objects.filter(
                mission_missionid=Mission.objects.get(missionid=mission_id)).order_by("-imagetimestamp")[start_number: end_number]
        mission_images = [image.as_dict() for image in requested_images]
        return send_response(mission_images)
    except Mission.DoesNotExist:
        return send_image_error("Mission does not exist")


def get_next_mission_images(mission_id, requested_datetime):
    requested_datetime_object = parse(requested_datetime)
    try:
        requested_images = Image.objects.filter(
                mission_missionid=Mission.objects.get(missionid=mission_id),
                imagetimestamp__gt=requested_datetime_object
                ).order_by("-imagetimestamp")
        mission_images = [image.as_dict() for image in requested_images]
        return send_response(mission_images)
    except Mission.DoesNotExist:
        return send_image_error("Mission does not exist")
    

def get_next_mission_images_via_image_id(mission_id, image_id, length):
    try:
        if length is None:
            requested_images = Image.objects.filter(
                mission_missionid=Mission.objects.get(missionid=mission_id),
                imageid__lt=image_id
                ).order_by("-imagetimestamp")
        else:
            requested_images = Image.objects.filter(
                mission_missionid=Mission.objects.get(missionid=mission_id),
                imageid__lt=image_id
            ).order_by("-imagetimestamp")[:length]
        mission_images = [image.as_dict() for image in requested_images]
        return send_response(mission_images)
    except Mission.DoesNotExist:
        return send_image_error("Mission does not exist")


def get_next_image_via_image_id(image_id, length):
    if length is None:
        requested_images = Image.objects.filter(
            imageid__lt=image_id
        ).order_by("-imagetimestamp")
    else:
        requested_images = Image.objects.filter(
            imageid__lt=image_id
        ).order_by("-imagetimestamp")[:length]
    images = [image.as_dict() for image in requested_images]
    return send_response(images)


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