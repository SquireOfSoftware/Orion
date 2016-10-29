from django.http import HttpResponse
from management_constants import DRONE_STATUS
import json

from rest.models import Drone
from rest.models import DroneStatus


def get_all_drones():
    drones = Drone.objects.all()

    return send_response([drone.as_dict() for drone in drones])


def get_drone(drone_id):
    requested_drone = Drone.objects.get(droneid=drone_id)

    if requested_drone is None:
        return get_drone_error("Could not locate drone with id: " + str(drone_id))

    return send_response(requested_drone.as_dict())


def add_a_drone(drone_object):
    print(drone_object)
    drone = json.loads(drone_object)

    drone_name = drone["name"]
    drone_ip = drone["ip"]

    drone_entry = Drone.objects.create(dronename=drone_name,
                                       droneip=drone_ip,
                                       dronestatus_dronestatusid=DroneStatus.objects.get(dronestatusname="IDLE"))

    return send_response(drone_entry.as_dict())


def verify_drone(drone_id):
    # drone can be found
    # drone id is IDLE
    for available_drone in registered_drones:
        if available_drone["drone"]["id"] == drone_id:
            return available_drone["drone"]["status"] == DRONE_STATUS["IDLE"]

    return False


# make sure that the drone with the drone id exists
def validate_drone(drone_id):
    for available_drone in registered_drones:
        if available_drone["drone"]["id"] == drone_id:
            return True
    return False


def update_drone(drone_object):
    requested_drone = json.loads(drone_object);
    for drone in registered_drones:
        if drone["drone"]["id"] == requested_drone["drone"]["id"]:
            registered_drones['count'] = change_details(drone, drone_object)


# mission error
def get_drone_error(message):
    return HttpResponse(json.dumps(
                        {"status": "error",
                         "data": message
                        }),
                        status=403)


def send_response(message):
    return HttpResponse(json.dumps(message))


def is_drone_busy(drone_id):
    try:
        drone = Drone.objects.get(droneid=drone_id)
        drone_status = DroneStatus.objects.get(dronestatusname="IDLE")
        print("Is drone busy? ", drone_status.dronestatusid != drone.dronestatus_dronestatusid.dronestatusid)
        return drone_status.dronestatusid != drone.dronestatus_dronestatusid.dronestatusid
    except Drone.DoesNotExist:
        print("Drone does not exist")
        return False