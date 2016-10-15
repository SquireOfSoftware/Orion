from management_constants import MISSION_STATUS
from drone_service import drones


class Queue(object):
    current_mission = None

    queued_missions = [{"mission": {
            "id": 1,
            "status": MISSION_STATUS['IN_PROGRESS'],
            "url": "missions/1",
            "waypoints": [ #floats 1 dec
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
                "url": "drones/01",
                "id": "01"
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
            "id": 2,
            "status": MISSION_STATUS['SUCCESS'],
            "url": "missions/2",
            "waypoints": [
                {"x": 0, "y": 0},
                {"x": 1, "y": 0},
                {"x": 2, "y": 0},
                {"x": 1, "y": 0},
                {"x": 0, "y": 0},
            ],
            "drone": {
                "url": "drones/02",
                "id": "02"
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
            "id": 3,
            "status": MISSION_STATUS['ABORTED'],
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

    def add_to_queue(self, mission):
        # add mission to the end of the queue
        self.queued_missions.append(mission)
        if not self.current_mission_is_running():
            self.current_mission = mission
            self.run_current_mission()

    def current_mission_is_running(self):
        return (self.current_mission is not None) and \
               (self.current_mission['mission']['status'] != MISSION_STATUS['IN_PROGRESS'])

    def get_mission(self, mission_id):
        for mission in self.queued_missions:
            if mission["mission"]["id"] == mission_id:
                return mission
        return None

    def get_total_no_of_missions(self):
        return len(self.queued_missions)

    def run_current_mission(self):
        if self.current_mission is not None:
            pass
        pass
