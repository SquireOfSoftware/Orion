from django.http import HttpResponse
import json

from rest.models import Drone
from rest.models import DroneStatus
from rest.models import Metadata

import mission_service


def get_all_drones():
    drones = Drone.objects.all()

    return send_response([drone.as_dict() for drone in drones])


def get_drone(drone_id):
    requested_drone = Drone.objects.get(droneid=drone_id)

    if requested_drone is None:
        return send_drone_error("Could not locate drone with id: " + str(drone_id))

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


# mission error
def send_drone_error(message):
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
        print("Is drone busy? ", drone.dronestatus_dronestatusid.dronestatusname != "IDLE")
        print(drone.dronestatus_dronestatusid.dronestatusname)
        return drone.dronestatus_dronestatusid.dronestatusname != "IDLE"
    except Drone.DoesNotExist:
        print("Drone does not exist")
        return False


def get_drone_status(drone_id):
    try:
        drone = Drone.objects.get(droneid=drone_id)
        return send_response({"status": drone.dronestatus_dronestatusid.dronestatusname})
    except Drone.DoesNotExist:
        return send_drone_error("Drone does not exist")


def get_drone_metadata(drone_id):
    '''
    Metadata.objects.create(
        metadatabattery=70,
        metadatastate=4,
        metadatamagx=10.1,
        metadatamagy=10.1,
        metadatamagz=10.1,
        metadatapressure=43,
        metadatatemp=34,
        metadatawindspeed=3,
        metadatawindangle=3,
        metadatawindcompangle=87,
        metadatarotx=4.3,
        metadataroty=4.3,
        metadatarotz=0,
        metadataaltitude=23,
        metadatavx=23,
        metadatavy=23,
        metadatavz=23,
        metadataax=23,
        metadataay=23,
        metadataaz=23,
        metadatamotor1=3,
        metadatamotor2=3,
        metadatamotor3=3,
        metadatamotor4=3,
        metadatatm=3,
        metadatatimestamp=mission_service.get_current_time(),
        drone_droneid=Drone.objects.get(droneid=1)
    )'''

    try:
        metadata = Metadata.objects.filter(drone_droneid=Drone.objects.get(droneid=drone_id))\
            .latest(field_name="metadatatimestamp")
        return send_response(metadata.as_dict())
    except Drone.DoesNotExist:
        return send_drone_error("Drone does not exist")
