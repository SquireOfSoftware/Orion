import json
from datetime import datetime
from subprocess import Popen

from django.http import HttpResponse

from drone_service import drones
from queue import Queue
from rest.models import Mission
from rest.models import Missionstatus
from rest.models import Drone
from rest.models import Waypoint
from rest.models import Obstacle
from rest.models import Pointofinterest

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

    altitude = data["mission"]["altitude"]
    drone_id = data['mission']['drone']['id']
    point_of_interest = data["mission"]["point_of_interest"]
    waypoints = data["mission"]["waypoints"]
    obstacles = data["mission"]["obstacles"]

    if drones.validate_drone(int(drone_id)):
        if not validate_altitude(altitude):
            return send_missions_error("Please verify that the altitude is between " +
                                       str(MIN_ALTITUDE) +
                                       " and " +
                                       str(MAX_ALTITUDE))
        elif not validate_point_of_interest(point_of_interest):
            return send_missions_error("Could not locate a point of interest")
        elif not validate_flight_path(waypoints, obstacles):
            return send_missions_error("Obstacles were found to be intersecting the flight path")
        elif not validate_battery():
            return send_missions_error("There is not enough battery to complete this flight path")
        else:
            # parses dictionary to json
            print("processing waypoints now")
            mission = create_mission(altitude, drone_id)
            print(mission)
            print(mission.missionid)
            # add all waypoints
            create_waypoints(mission.missionid, waypoints)
            # processed_waypoints = [wp.as_dict() for wp in create_waypoints(1, waypoints)]
            # add all obstacles
            create_obstacles(mission.missionid, obstacles)
            # processed_obstacles = [ob.as_dict() for ob in create_obstacles(1, obstacles)]
            # add point of interest
            create_point_of_interest(mission.missionid, point_of_interest)
            # processed_point_of_interest = create_point_of_interest(1, point_of_interest).as_dict()
            return HttpResponse(json.dumps(mission.as_dict()))
            #return HttpResponse(json.dumps(processed_point_of_interest))

    return send_missions_error("Drone with id " + str(drone_id) + " is not available")


def create_mission(altitude, drone_id):
    mission = Mission.objects.create(
        missioncreationdate=datetime.now().__str__(),
        missionaltitude=float(altitude),
        missionstatus_missionstatustid=Missionstatus.objects.get(missionstatusid=MISSION_STATUS["QUEUED"]),
        drone_droneid=Drone.objects.get(droneid=drone_id)
    )
    mission.save()
    return mission


def create_waypoints(mission_id, waypoint_array):
    waypoints = []
    for waypoint in waypoint_array:
        print(mission_id)
        points_are_valid = validate_points(waypoint)
        if points_are_valid:
            waypoints.append(Waypoint.objects.create(
                waypointx=float(waypoint["x"]),
                waypointy=float(waypoint["y"]),
                mission_missionid=Mission.objects.get(missionid=mission_id)
            ))
    print(waypoints)
    return waypoints


def create_obstacles(mission_id, obstacle_array):
    obstacles = []
    for obstacle in obstacle_array:
        points_are_valid = validate_points(obstacle)
        if points_are_valid:
            obstacles.append(Obstacle.objects.create(
                obstaclecoordinatex=float(obstacle["x"]),
                obstaclecoordinatey=float(obstacle["y"]),
                mission_missionid=Mission.objects.get(missionid=mission_id)
            ))
    return obstacles


def create_point_of_interest(mission_id, point_of_interest):
    # assume there is only one point of interest
    poi = Pointofinterest.objects.create(
        pointofinterestx=float(point_of_interest[0]["x"]),
        pointofinteresty=float(point_of_interest[0]["y"]),
        mission_missionid=Mission.objects.get(missionid=mission_id)
    )
    return poi


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


def validate_points(point):
    return (point["x"] >= MIN_X) and \
           (point["x"] <= MAX_X) and \
           (point["y"] >= MIN_Y) and \
           (point["y"] <= MAX_Y)


def validate_point_of_interest(point):
    # verify that it exists
    # verify that it is within the boundaries of 3m by 3m

    return (point[0]["x"] > MIN_X) and \
           (point[0]["x"] < MAX_X) and \
           (point[0]["y"] > MIN_Y) and \
           (point[0]["y"] < MAX_Y)


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