from django.http import HttpResponse
from management_constants import DRONE_STATUS
import json

registered_drones = [
    {
        "drone": {
            "id": 1,
            "url": "/drones/1",
            "status": DRONE_STATUS["IDLE"]
        }
    }
]


def get_all_drones():
    return HttpResponse(json.dumps(registered_drones))


def get_drone(drone_id):

    requested_drone = find_drone(drone_id)

    if requested_drone is None:
        return get_drone_error("Could not locate drone with id: " + str(drone_id))

    return HttpResponse(json.dumps(requested_drone))


def find_drone(drone_id):
    for drone in registered_drones:
        if drone["drone"]["id"] == drone_id:
            return drone
    return None


# mission error
def get_drone_error(message):
    return HttpResponse(json.dumps(
                        {"status": "error",
                         "data": message
                        }),
                        status=403)