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
    $scope.baseurl = "http://localhost:5000";
    $scope.warningMsg = "";
    $scope.canvasGrid = null;

    $scope.currentMission = {};

    var MINGRID = 0;
    var MAXGRID = 300;

    $scope.init = function() {
        $(".mission-page").hide();
        $("#select-a-drone-page").show();
        initialiseDrones();
    };

    function initialiseDrones() {
        addDrone(setupDrone("voyager", "Voyager", "../../images/Drone1.png"));
        addDrone(setupDrone("sputnik", "Sputnik", "../../images/Drone2.png"));
    }

    function initialiseGrid() {
        var canvasGrid = jQuery("#canvas-test")[0].getContext('2d');
        $log.log(canvasGrid[0]);
        canvasGrid = drawVerticalLines(canvasGrid);
        canvasGrid = drawHorizontalLines(canvasGrid);
        $scope.canvasGrid = canvasGrid;
    }

    function drawVerticalLines(canvasGrid) {
        for (var x = 0; x <= 300; x += 10) {
            canvasGrid.moveTo(x, MINGRID);
            canvasGrid.lineTo(x, MAXGRID);
            canvasGrid.stroke();
        }
        return canvasGrid;
    }

    function drawHorizontalLines(canvasGrid) {
        for (var y = 0; y <= 300; y += 10) {
            canvasGrid.moveTo(MINGRID, y);
            canvasGrid.lineTo(MAXGRID, y);
            canvasGrid.stroke();
        }
        return canvasGrid;
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
        initialiseGrid();
    };

    $scope.selectDrone = function (selectedDrone) {
        $log.log("drone with id: " + selectedDrone.id + " has been selected.");

        $scope.selectedDrone = selectedDrone;
        jQuery("#selected-drone-message").show();
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

            var url = $scope.baseurl + "/testREST";
            $log.log(currentMission);

            var request = {
                url: url,
                method: 'GET',
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE',
                    'Access-Control-Max-Age': '3600',
                    'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
                    'Content-Type': 'application/text',
                    'Access-Control-Allow-Credentials': false
                }
                //data: currentMission
            };
            $log.log(request);

            /*$http.post(
                url,
                currentMission, function(data) {
                $log.log(data);
                $log.log(typeof(data));
            });*/
            $http(request).then(function(data) {
                $log.log(data);
                $log.log(typeof(data));
            });
        }

    };
});