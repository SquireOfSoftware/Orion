from django.http import HttpResponse
import drone_service
import mission_service

def index(request):
    pass


def handle_missions(request):
    # https://docs.djangoproject.com/en/1.10/topics/http/urls/#how-django-processes-a-request
    print(request.body)
    if request.method == "GET":
        return mission_service.get_all_missions();
    elif (request.method == "POST") and (request.body != ""):
        return mission_service.add_a_mission(request.body)
    return respond_with_error("Invalid METHOD " + request.method)


def get_mission(request, mission_id):
    if request.method == "GET":
        return mission_service.get_mission(int(mission_id))
    return respond_with_error("Invalid METHOD " + request.method)


# pass through anything relating to drones
def handle_drones(request):
    if request.method == "GET":
        return drone_service.get_all_drones();
    elif (request.method == "POST") and (request.body != ""):
        return drone_service.add_a_drone(request.body)
    return respond_with_error("Invalid METHOD " + request.method)


def get_drone(request, drone_id):
    if request.method == "GET":
        return drone_service.get_drone(int(drone_id))
    return respond_with_error("Invalid METHOD " + request.method)


def control_drone(request, id):
    pass

# process anything relating to images
# need to know how many, pull out query
def get_images(request):
    pass


def get_image(request, image_id):
    pass


# get literally the current image regardless of mission
def get_current_image(self):
    pass


def get_mission_images(mission_id):
    pass


def respond_with_error(message):
    return HttpResponse(json.dumps(
        {"status": "error",
         "data": message
         }),
        status=403)