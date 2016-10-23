import json
from django.utils import timezone
from subprocess import Popen

from django.http import HttpResponse

from drone_service import drones
from rest.models import Mission
from rest.models import Missionstatus
from rest.models import Drone
from rest.models import DroneStatus
from rest.models import Waypoint
from rest.models import Obstacle
from rest.models import Pointofinterest

from management_constants import MISSION_STATUS
from management_constants import DRONE_STATUS


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


# adding a missions
def add_a_mission(data):
    # parses string to dictionary
    data = json.loads(data)

    print(data)
    altitude = float(data["altitude"])
    drone_id = int(data['selectedDrone']['id'])
    point_of_interest = data["pointOfInterest"]
    waypoints = data["waypoints"]
    obstacles = data["obstacles"]

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
            # add all waypoints
            create_waypoints(mission.missionid, waypoints)
            # add all obstacles
            create_obstacles(mission.missionid, obstacles)
            # add point of interest
            create_point_of_interest(mission.missionid, point_of_interest)
            return HttpResponse(json.dumps(mission.as_dict()))

    return send_missions_error("Drone with id " + str(drone_id) + " is not available")


def create_mission(altitude, drone_id):
    mission = Mission.objects.create(
        missioncreationdate=get_current_time(),
        missionaltitude=float(altitude),
        missionstatus_missionstatusid=Missionstatus.objects.get(missionstatusid=MISSION_STATUS["QUEUED"]),
        drone_droneid=Drone.objects.get(droneid=drone_id)
    )
    return mission


def create_waypoints(mission_id, waypoint_array):
    waypoints = []
    for waypoint in waypoint_array:
        points_are_valid = validate_points(waypoint)
        if points_are_valid:
            waypoints.append(Waypoint.objects.create(
                waypointx=float(waypoint["x"]),
                waypointy=float(waypoint["y"]),
                mission_missionid=Mission.objects.get(missionid=mission_id)
            ))
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
        pointofinterestx=float(point_of_interest["x"]),
        pointofinteresty=float(point_of_interest["y"]),
        mission_missionid=Mission.objects.get(missionid=mission_id)
    )
    return poi


# this includes aborting a mission
def start_mission(mission_id):
    mission = Mission.objects.get(missionid=mission_id)
    print(mission)
    no_missions_are_running = verify_no_missions_are_active()
    drone_is_available = verify_drone_is_available(mission.drone_droneid.droneid)
    if (mission is not None) and no_missions_are_running and drone_is_available:
        mission.missionstatus_missionstatusid = Missionstatus.objects.get(missionstatusid=MISSION_STATUS["IN_PROGRESS"])
        mission.save()

        drone = Drone.objects.get(droneid=mission.drone_droneid.droneid)
        drone.dronestatus_dronestatusid = DroneStatus.objects.get(dronestatusid=DRONE_STATUS["TAKING OFF"])
        drone.save()

        Popen("python experiments/process_spawnee.py", shell=True)

        return send_response(mission.as_dict())
    elif mission is None:
        return send_missions_error("Could not locate mission with id: " + str(mission_id))
    elif no_missions_are_running is not True:
        return send_missions_error("There is already a mission running.")
    elif drone_is_available is not True:
        return send_missions_error("The drone for this mission is currently unavailable.")

    return send_missions_error("An error has occurred.")


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
    x = int(point["x"])
    y = int(point["y"])

    return (x > MIN_X) and \
           (x < MAX_X) and \
           (y > MIN_Y) and \
           (y < MAX_Y)


def validate_flight_path(waypoints, obstacles):
    # for now assume there are no obstacles
    # TODO implement this feature to work with flight path
    return True


def validate_battery():
    # assume there is enough battery charge
    # TODO implement this feature to work with the drone metedata
    return True


def verify_no_missions_are_active():
    try:
        active_mission = Mission.objects.get(missionstatus_missionstatusid=MISSION_STATUS["IN_PROGRESS"])
        return active_mission is None
    except Mission.DoesNotExist:
        return True


def verify_drone_is_available(drone_id):
    try:
        drone_status = DroneStatus.objects.get(
            dronestatusid=Drone.objects.get(droneid=drone_id).dronestatus_dronestatusid.dronestatusid)
        return drone_status.dronestatusid == DRONE_STATUS["IDLE"]
    except Drone.DoesNotExist:
        return False

# mission error
def send_missions_error(message):
    return HttpResponse(json.dumps({"status": "error",
                                    "data": message
                                    }),
                        status=403)


def add_a_mission_error():
    return send_missions_error("Invalid request only POST allowed on this end point")


def send_response(message):
    return HttpResponse(json.dumps(message))


def get_current_time():
    time = timezone.now().__str__()
    return time
