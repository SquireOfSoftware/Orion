from django.http import HttpResponse
from django.http import HttpRequest
import mission_service

# Create your views here.


def index(request):
    pass


def get_all_missions(request):
    # https://docs.djangoproject.com/en/1.10/topics/http/urls/#how-django-processes-a-request
    print(request.method);
    if request.method == "GET":
        return mission_service.get_all_missions();
    elif request.method == "POST":
        return mission_service.add_a_mission(request)
    return mission_service.get_missions_error("Invalid METHOD " + request.method)


def get_mission(request, mission_id):
    if request.method == "GET":
        return mission_service.get_mission(mission_id)
    return mission_service.add_a_mission_error()


# pass through anything relating to drones
def get_drones(request):
    pass


def get_drone(request, id):
    pass


def control_drone(request, id):
    pass

# process anything relating to images
# need to know how many, pull out query
def get_images(request):
    pass


def get_image(request, id):
    pass


# get literally the current image regardless of mission
def get_current_image(self):
    pass


def get_mission_images(mission_id):
    pass