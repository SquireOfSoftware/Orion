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


def find_drone(self, drone_id):
    for drone in self.registered_drones:
        if drone["drone"]["id"] == drone_id:
            return drone
    return None


def add_a_drone(self, drone_object):
    drone = json.loads(drone_object)

    drone["drone"]["id"] = len(self.registered_drones) + 1
    drone["drone"]["status"] = DRONE_STATUS["IDLE"]
    drone["drone"]["url"] = "drones/" + str(drone["drone"]["id"])

    self.registered_drones.append(drone)

    return HttpResponse(json.dumps(drone))


def verify_drone(self, drone_id):
    # drone can be found
    # drone id is IDLE
    for available_drone in self.registered_drones:
        if available_drone["drone"]["id"] == drone_id:
            return available_drone["drone"]["status"] == DRONE_STATUS["IDLE"]

    return False


# make sure that the drone with the drone id exists
def validate_drone(self, drone_id):
    for available_drone in self.registered_drones:
        if available_drone["drone"]["id"] == drone_id:
            return True
    return False


def update_drone(self, drone_object):
    requested_drone = json.loads(drone_object);
    for drone in self.registered_drones:
        if drone["drone"]["id"] == requested_drone["drone"]["id"]:
            self.registered_drones['count'] = change_details(drone, drone_object)


# mission error
def get_drone_error(message):
    return HttpResponse(json.dumps(
                        {"status": "error",
                         "data": message
                        }),
                        status=403)


def send_response(message):
    return HttpResponse(json.dumps(message))