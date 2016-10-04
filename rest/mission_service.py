from django.http import HttpResponse
import json
import mission_status


def get_missions():
    # TODO write the get function for missions
    return HttpResponse(json.dumps({"status": mission_status.SUCCESS,
                                    "data": [{"id": "00001", "status": mission_status.IN_PROGRESS},
                                                 {"id": "00002", "status": mission_status.IDLE}
                                                 ]}));


def get_mission(request, id):
    # TODO write the search function for a mission
    return HttpResponse(json.dumps({"data": {"id": id,
                                                "status": mission_status.IN_PROGRESS
                                                }}));


def get_missions_error():
    return HttpResponse(json.dumps({"status": "error",
                                    "data": "Invalid request only GET allowed on this end point"
                                    }), status=403)


def add_a_mission(data):
    return HttpResponse(json.dumps({"status": mission_status.SUCCESS,
                                    "data": {"id": id,
                                             "status": mission_status.IN_PROGRESS
                                             }}));


def add_a_mission_error():
    return HttpResponse(json.dumps({"status": mission_status.FAILED,
                                    "data": "Invalid request only POST allowed on this end point"
                                    }), status=403)

# this includes aborting a mission
def update_mission(data):
    pass