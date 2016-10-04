/**
 * Created by Joseph Tran on 1/10/2016.
 * This is a helpful REST API
 * https://thinkster.io/django-angularjs-tutorial
 *
 * AngularJS tutorial
 * https://www.toptal.com/angular-js/a-step-by-step-guide-to-your-first-angularjs-app
 */

var webServer = angular.module("webServer", [])
.controller("missionCtrl", function($log, $http, $scope)
{
    $scope.drones = [];
    $scope.selectedDrone = {};
    $scope.baseurl = "http://localhost:80";
    $scope.warningMsg = "";

    $scope.currentMission = {};

    $scope.init = function() {
        $(".mission-page").hide();
        $("#select-a-drone-page").show();
        initialiseDrones();
    };

    function initialiseDrones() {
        addDrone(setupDrone("voyager", "Voyager", "../../images/Drone1.png"));
        addDrone(setupDrone("sputnik", "Sputnik", "../../images/Drone2.png"));
    }

    function setupDrone(id, name, imagePath) {
        return {
            id: id,
            name: name,
            image: imagePath
        };
    }

    function addDrone(drone) {
        $scope.drones.push(drone);
    }

    $log.debug("Hello world");

    $scope.currentMission = {};

    $scope.sayHiForMe = function () {
        $log.debug("YOU CLICKED ME!");
        jQuery("#select-a-drone-page").hide();
        jQuery("#configure-mission-page").show();
    };

    $scope.selectDrone = function (selectedDrone) {
        $log.log("drone with id: " + selectedDrone.id + " has been selected.");

        $scope.selectedDrone = selectedDrone;
    };

    $scope.submitMission = function () {
        var selectedDrone = $scope.selectedDrone;

        if (selectedDrone == undefined ||
            selectedDrone == null)
            $log.log("An undefined selectedDrone");
        else {
            $log.log($scope.selectedDrone.id);
            $log.log("Mission has been started");


            var currentMission = {
                selectedDrone: selectedDrone.id,
                waypoints: [
                    // move three blocks
                    {"x": 0, "y": 0},
                    {"x": 0, "y": 1},
                    {"x": 0, "y": 2},
                    {"x": 1, "y": 2},
                    {"x": 2, "y": 2},
                    {"x": 2, "y": 1},
                    {"x": 2, "y": 0}
                ],
                altitude: 1,
                obstacles: [],
                pointOfInterest: {"x": 1, "y": 1}
            };

            var url = $scope.baseurl + "/create/mission";
            $log.log(currentMission);

            $http.post(url, {
                "message": currentMission
            });
        }

    };
});