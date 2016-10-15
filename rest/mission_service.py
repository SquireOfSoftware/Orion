from django.http import HttpResponse
import json
from queue import Queue
from datetime import datetime
from drone_service import drones

missions_queued = Queue()

MIN_ALTITUDE = 0.5
MAX_ALTITUDE = 2.5

MIN_X = 0
MAX_X = 3.0
MIN_Y = 0
MAX_Y = 3.0


# get all the missions
def get_all_missions():
    # TODO write the get function for missions
    return HttpResponse(json.dumps(missions_queued.queued_missions))


# get a single missions
def get_mission(mission_id):
    # TODO write the search function for a mission
    mission = missions_queued.get_mission(mission_id=mission_id)

    if mission is None:
        return get_missions_error("Could not find mission with id: " + str(mission_id))

    return HttpResponse(json.dumps(mission))


# mission error
def get_missions_error(message):
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
            return get_missions_error("Please verify that the altitude is between " +
                                      str(MIN_ALTITUDE) +
                                      " and " +
                                      str(MAX_ALTITUDE))
        elif not validate_point_of_interest(data["mission"]["point_of_interest"]):
            return get_missions_error("Could not locate a point of interest")
        elif not validate_flight_path(data["mission"]["waypoints"], data["mission"]["obstacles"]):
            return get_missions_error("Obstacles were found to be intersecting the flight path")
        elif not validate_battery():
            return get_missions_error("There is not enough battery to complete this flight path")
        else:
            # parses dictionary to json
            missions_queued.add_to_queue(mission=data)

            return HttpResponse(json.dumps(data))

    return get_missions_error("Drone with id " + str(drone_id) + " is not available")


def add_a_mission_error():
    return get_missions_error("Invalid request only POST allowed on this end point")


# this includes aborting a mission
def update_mission(data):
    pass


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
    return (point_of_interest["x"] > MIN_X) and \
           (point_of_interest["x"] < MAX_X) and \
           (point_of_interest["y"] > MIN_Y) and \
           (point_of_interest["y"] < MAX_Y)


def validate_flight_path(waypoints, obstacles):
    # for now assume there are no obstacles
    # TODO implement this feature to work with flight path
    return True


def validate_battery():
    # assume there is enough battery charge
    # TODO implement this feature to work with the drone metedata
    return True
