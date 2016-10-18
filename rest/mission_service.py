import json
from datetime import datetime
from subprocess import Popen

from django.http import HttpResponse

from drone_service import drones
from queue import Queue
from rest.models import Mission
from rest.models import Missionstatus
from rest.models import Drone

from management_constants import MISSION_STATUS
from management_constants import DRONE_STATUS

missions_queued = Queue()

MIN_ALTITUDE = 0.5
MAX_ALTITUDE = 2.5

MIN_X = 0
MAX_X = 3.0
MIN_Y = 0
MAX_Y = 3.0

missions_test = []


# get all the missions
def get_all_missions():
    # TODO write the get function for missions
    missions_query = Mission.objects.all()
    missions_query_dictionary = [mission.as_dict() for mission in missions_query]
    return HttpResponse(
        json.dumps(missions_query_dictionary)
    )


# get a single missions
def get_mission(mission_id):
    # TODO write the search function for a mission
    mission = Mission.objects.get(missionid=mission_id)
    if mission is None:
        return send_missions_error("Could not find mission with id: " + str(mission.missionid))

    return HttpResponse(json.dumps(mission.as_dict()))


# mission error
def send_missions_error(message):
    return HttpResponse(json.dumps({"status": "error",
                                    "data": message
                                    }),
                        status=403)


# adding a missions
def add_a_mission(data):
    # parses string to dictionary
    data = json.loads(data)

    data['mission']['id'] = missions_queued.get_total_no_of_missions() + 1
    data['mission']['start_time'] = datetime.now().__str__()
    data['mission']['status'] = int(data['mission']['status'])
    data['mission']['url'] = "missions/" + str(data['mission']['id'])

    drone_id = data['mission']['drone']['id']

    if drones.validate_drone(int(drone_id)):
        if not validate_altitude(data["mission"]["altitude"]):
            return send_missions_error("Please verify that the altitude is between " +
                                       str(MIN_ALTITUDE) +
                                       " and " +
                                       str(MAX_ALTITUDE))
        elif not validate_point_of_interest(data["mission"]["point_of_interest"]):
            return send_missions_error("Could not locate a point of interest")
        elif not validate_flight_path(data["mission"]["waypoints"], data["mission"]["obstacles"]):
            return send_missions_error("Obstacles were found to be intersecting the flight path")
        elif not validate_battery():
            return send_missions_error("There is not enough battery to complete this flight path")
        else:
            # parses dictionary to json
            # missions_queued.add_to_queue(mission=data)
            mission = Mission.objects.create(
                missioncreationdate=datetime.now().__str__(),
                missionaltitude=float(data["mission"]["altitude"]),
                missionstatus_missionstatustid=Missionstatus.objects.get(missionstatusid=MISSION_STATUS["QUEUED"]),
                drone_droneid=Drone.objects.get(droneid=drone_id)
            )
            return HttpResponse(json.dumps(mission.as_dict()))

    return send_missions_error("Drone with id " + str(drone_id) + " is not available")


def add_a_mission_error():
    return send_missions_error("Invalid request only POST allowed on this end point")


# this includes aborting a mission
def start_mission(data, mission_id):
    data = json.loads(data)
    mission = missions_queued.get_mission(int(mission_id))
    if (mission is not None) and (verify_no_missions_are_active()):
        Popen("python experiments/process_spawnee.py", shell=True)
        return send_response(missions_queued.update_mission(data))
    return send_missions_error("Could not locate mission with id: " + str(data["mission"]["id"]))


def validate_mission(mission):
    return validate_altitude(mission["mission"]["altitude"]) and \
           validate_point_of_interest(mission["mission"]["point_of_interest"]) and \
           validate_flight_path(mission["mission"]["waypoints"], mission["mission"]["obstacles"]) and \
           validate_battery()


def validate_altitude(altitude):
    # validate in accordance with spatial restrictions of 50cm to 2.5m
    return (altitude > MIN_ALTITUDE) and (altitude < MAX_ALTITUDE)


def validate_point_of_interest(point_of_interest):
    # verify that it exists
    # verify that it is within the boundaries of 3m by 3m
    return (point_of_interest[0]["x"] > MIN_X) and \
           (point_of_interest[0]["x"] < MAX_X) and \
           (point_of_interest[0]["y"] > MIN_Y) and \
           (point_of_interest[0]["y"] < MAX_Y)


def validate_flight_path(waypoints, obstacles):
    # for now assume there are no obstacles
    # TODO implement this feature to work with flight path
    return True


def validate_battery():
    # assume there is enough battery charge
    # TODO implement this feature to work with the drone metedata
    return True


def verify_no_missions_are_active():
    return missions_queued.is_any_mission_active()


def send_response(message):
    return HttpResponse(json.dumps(message))