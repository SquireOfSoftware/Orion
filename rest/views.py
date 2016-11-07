from django.http import HttpResponse
import drone_service
import mission_service
import image_service
import json

from django.views.decorators.csrf import csrf_exempt


def index(request):
    pass


@csrf_exempt
def handle_missions(request):
    # https://docs.djangoproject.com/en/1.10/topics/http/urls/#how-django-processes-a-request
    if request.method == "GET":
        return mission_service.get_all_missions()
    elif (request.method == "POST") and (request.body != ""):
        return mission_service.add_a_mission(request.body)
    return respond_with_error("Invalid METHOD " + request.method)


@csrf_exempt
def start_mission(request, mission_id):
    # check if mission with id exists
    # check if mission status is not in progress
    # change the mission status
    # spawn process
    if request.method == "PUT":
        return mission_service.start_mission(mission_id)
    return respond_with_error("Invalid METHOD " + request.method)


def get_mission(request, mission_id):
    if request.method == "GET":
        return mission_service.get_mission(int(mission_id))
    return respond_with_error("Invalid METHOD " + request.method)


def get_mission_waypoints(request, mission_id):
    if request.method == "GET":
        return mission_service.get_mission_waypoints(int(mission_id))
    return respond_with_error("Invalid METHOD " + request.method)


def get_mission_status(request, mission_id):
    if request.method == "GET":
        return mission_service.get_mission_status(int(mission_id))
    return respond_with_error("Invalid METHOD " + request.method)


# pass through anything relating to drones
@csrf_exempt
def handle_drones(request):
    if request.method == "GET":
        return drone_service.get_all_drones()
    elif (request.method == "POST") and (request.body != ""):
        return drone_service.add_a_drone(request.body)
    return respond_with_error("Invalid METHOD " + request.method)


def get_drone(request, drone_id):
    if request.method == "GET":
        return drone_service.get_drone(int(drone_id))
    return respond_with_error("Invalid METHOD " + request.method)


def control_drone(request, id):
    pass


def get_drone_status(request, drone_id):
    if request.method == "GET":
        return drone_service.get_drone_status(int(drone_id))
    return respond_with_error("Invalid METHOD " + request.method)


def get_drone_current_metadata(request, drone_id):
    if request.method == "GET":
        return drone_service.get_drone_metadata(int(drone_id))
    return respond_with_error("Invalid METHOD " + request.method)


# process anything relating to images
# need to know how many, pull out query
def get_images(request):
    if request.method == "GET":
        start_number = request.GET.get("start_number")
        end_number = request.GET.get("end_number")
        if (start_number is not None) and (end_number is not None):
            return image_service.get_images(int(start_number), int(end_number))
        elif start_number is not None:
            return image_service.get_images(int(start_number), int(start_number) + 10)
        else:
            # default to first 10 images
            return image_service.get_images(0, 10)
    return respond_with_error("Invalid METHOD " + request.method)


def get_image(request, image_id):
    pass


# get literally the current image regardless of mission
def get_current_image(request):
    return image_service.get_current_image()


def get_mission_images(request, mission_id):
    if request.method == "GET":
        start_number = request.GET.get("start_number")
        end_number = request.GET.get("end_number")
        if (start_number is not None) and (end_number is not None):
            return image_service.get_mission_images(int(mission_id), int(start_number), int(end_number))
        elif start_number is not None:
            print(start_number)
            return image_service.get_mission_images(int(mission_id), int(start_number), int(start_number) + 10)
        elif end_number is not None:
            if int(end_number) <= 10:
                return image_service.get_mission_images(int(mission_id), 0, int(end_number))
            elif int(end_number) > 10:
                return image_service.get_mission_images(int(mission_id), int(end_number) - 10, int(end_number))
        else:
            # default to first 10 images
            return image_service.get_mission_images(int(mission_id), 0, 10)
    return respond_with_error("Invalid METHOD " + request.method)


def get_next_set_of_mission_images(request, mission_id):
    if request.method == "GET":
        datetime = request.GET.get("datetime")
        if datetime is not None:
            return image_service.get_next_mission_images(int(mission_id), datetime)
        return respond_with_error("Not date was found")
    return respond_with_error("Invalid METHOD " + request.method)


def get_next_set_of_mission_images_via_image_id(request, mission_id, image_id):
    if request.method == "GET":
        length = request.GET.get("length")
        if length is None:
            return image_service.get_next_mission_images_via_image_id(int(mission_id), int(image_id), length=None)
        return image_service.get_next_mission_images_via_image_id(int(mission_id), int(image_id), int(length))
    return respond_with_error("Invalid METHOD " + request.method)


def get_next_image_set(request, image_id):
    if request.method == "GET":
        length = request.GET.get("length")
        print(length)
        if length is None:
            return image_service.get_next_image_via_image_id(int(image_id), length=None)
        return image_service.get_next_image_via_image_id(int(image_id), int(length))
    return respond_with_error("Invalid METHOD " + request.method)


def respond_with_error(message):
    return HttpResponse(json.dumps(
        {"status": "error",
         "data": message
         }),
        status=403)


def post_test_image(request, mission_id):
    if request.method == "POST":
        return image_service.post_images(request.body, int(mission_id))
    return respond_with_error("Invalid METHOD " + request.method)