from django.http import HttpResponse
import drone_service
import mission_service
import image_service
import json


def index(request):
    pass


def handle_missions(request):
    # https://docs.djangoproject.com/en/1.10/topics/http/urls/#how-django-processes-a-request
    if request.method == "GET":
        return mission_service.get_all_missions()
    elif (request.method == "POST") and (request.body != ""):
        return mission_service.add_a_mission(request.body)
    return respond_with_error("Invalid METHOD " + request.method)


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


def get_mission_images(mission_id):
    pass


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