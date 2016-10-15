from django.http import HttpResponse
import json
from queue import Queue
from datetime import datetime
from drone_service import drones

missions_queued = Queue()

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
    return HttpResponse(json.dumps(
                        {"status": "error",
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
    data['mission']['url'] = "drones/" + str(data['mission']['id'])

    drone_id = data['mission']['drone']['id']

    if drones.validate_drone(int(drone_id)):
        # parses dictionary to json
        missions_queued.add_to_queue(mission=data)

        return HttpResponse(json.dumps(data));

    return get_missions_error("Drone with id " + str(drone_id) + " is not available")


def add_a_mission_error():
    return get_missions_error("Invalid request only POST allowed on this end point")


# this includes aborting a mission
def update_mission(data):
    pass