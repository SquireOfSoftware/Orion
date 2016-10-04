from django.shortcuts import render
import mission_service

# Create your views here.

def index(request):
    pass

def get_all_missions(request):

    # https://docs.djangoproject.com/en/1.10/topics/http/urls/#how-django-processes-a-request

    print(request.method);
    if request.method == "GET":
        print(request.content_params)
        return mission_service.get_missions();

    return mission_service.get_missions_error()

def get_mission(request, id):
    if request.method == "GET":
        return mission_service.get_mission(request, id)

    return mission_service.add_a_mission_error()

def drones(request):
    pass

def media(request):
    pass
