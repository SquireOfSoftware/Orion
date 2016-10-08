from mission_status import MISSION_STATUS


class Queue(object):
    current_mission = None

    queued_missions = [{"mission": {
            "id": "00001",
            "status": MISSION_STATUS['IN_PROGRESS'],
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

    def add_to_queue(self, mission):
        # add mission to the end of the queue
        print(type(mission))
        self.queued_missions.append(mission)
        if not self.current_mission_is_running():
            self.current_mission = mission
            self.run_current_mission()

    def current_mission_is_running(self):
        return (self.current_mission is not None) and \
               (self.current_mission['mission']['status'] != MISSION_STATUS['IN_PROGRESS'])

    def get_mission(self, mission_id):
        return self.queued_missions[mission_id];

    def get_total_no_of_missions(self):
        return len(self.queued_missions)

    def run_current_mission(self):
        if self.current_mission is not None:
            pass