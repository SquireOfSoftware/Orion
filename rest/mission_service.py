from django.http import HttpResponse
import json
import mission_status
from datetime import datetime

missions = [{"mission": {
        "id": "00001",
        "status": mission_status.IN_PROGRESS,
        "url": "missions/1",
        "waypoints": [
            {"x": 0, "y": 0},
            {"x": 1, "y": 0},
            {"x": 2, "y": 0},
            {"x": 2, "y": 1},
            {"x": 2, "y": 2},
            {"x": 1, "y": 2},
            {"x": 0, "y": 2},
            {"x": 0, "y": 1},
            {"x": 0, "y": 0}
        ],
        "drone": {
            "id": "01",
            "name": "sputnik",
            "url": "drones/01"
        },
        "altitude": 1,
        "point_of_interest": [
            {"x": 1, "y": 1}
        ],
        "start_time": 1,
        "finish_time": -1,
        "obstacles": []
    }},
    {"mission": {
        "id": "00002",
        "status": mission_status.SUCCESS,
        "url": "missions/2",
        "waypoints": [
            {"x": 0, "y": 0},
            {"x": 1, "y": 0},
            {"x": 2, "y": 0},
            {"x": 1, "y": 0},
            {"x": 0, "y": 0},
        ],
        "drone": {
            "id": "02",
            "name": "pioneer",
            "url": "drones/02"
        },
        "altitude": 1,
        "point_of_interest": [
            {"x": 1, "y": 1}
        ],
        "start_time": 1,
        "finish_time": 5,
        "obstacles": [
            {"x": 1, "y": 1}
        ]
    }},
    {"mission": {
        "id": "00003",
        "status": mission_status.ABORTED,
        "url": "missions/3",
        "waypoints": [
            {"x": 0, "y": 0},
            {"x": 0, "y": 1},
            {"x": 0, "y": 2},
            {"x": 0, "y": 1},
            {"x": 0, "y": 0},
        ],
        "drone": {
            "id": "04",
            "name": "dennis",
            "url": "drones/04"
        },
        "altitude": 1,
        "point_of_interest": [
            {"x": 1, "y": 1}
        ],
        "start_time": 1,
        "finish_time": 5,
        "obstacles": [
            {"x": 1, "y": 1}
        ]
    }}
]

# get all the missions
def get_all_missions():
    # TODO write the get function for missions
    return HttpResponse(json.dumps(missions))


# get a single missions
def get_mission(mission_id):
    # TODO write the search function for a mission
    return HttpResponse(json.dumps(missions[int(mission_id)]))


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

    data['mission']['id'] = len(missions) + 1
    data['mission']['start_time'] = datetime.now().__str__()

    # parses dictionary to json
    missions.append(json.dumps(data))

    return HttpResponse(json.dumps(
        data
    ));


def add_a_mission_error():
    return get_missions_error("Invalid request only POST allowed on this end point")


# this includes aborting a mission
def update_mission(data):
    pass