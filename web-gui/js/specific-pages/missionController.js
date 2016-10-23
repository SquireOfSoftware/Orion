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
    $scope.baseurl = "http://localhost:5001";
    $scope.warningMsg = "";

    $scope.currentMission = {};

    var MINGRID = 0;
    var MAXGRID = 300;

    var globalCanvasGrid = null;
    var canvasOffsets = {};

    $scope.currentWaypoints = [];

    $scope.init = function() {
        $(".mission-page").hide();
        $("#select-a-drone-page").show();
        initialiseDrones();
    };

    /*
    * This is for the first screen
    * */

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
        initialiseGrid();
    };

    $scope.selectDrone = function (selectedDrone) {
        $log.debug("drone with id: " + selectedDrone.id + " has been selected.");

        $scope.selectedDrone = selectedDrone;
        jQuery("#selected-drone-message").show();
    };

    /*
    * This is for the grid screen
    * */

    function initialiseGrid() {
        var canvasObject = jQuery("#canvas-test")[0];
        canvasObject.addEventListener("mousedown", triggerMouseClick, false);
        var canvasGrid = canvasObject.getContext('2d');
        getScale(canvasObject);
        getOffsets(canvasObject);
        canvasGrid = drawVerticalLines(canvasGrid);
        canvasGrid = drawHorizontalLines(canvasGrid);
        globalCanvasGrid = canvasGrid;
    }

    function drawVerticalLines(canvasGrid) {
        for (var x = 0; x <= 300; x += 50) {
            canvasGrid.moveTo(x, MINGRID);
            canvasGrid.lineTo(x, MAXGRID);
            canvasGrid.stroke();
        }
        return canvasGrid;
    }

    function drawHorizontalLines(canvasGrid) {
        for (var y = 0; y <= 300; y += 50) {
            canvasGrid.moveTo(MINGRID, y);
            canvasGrid.lineTo(MAXGRID, y);
            canvasGrid.stroke();
        }
        return canvasGrid;
    }

    function getScale(canvasObject) {
        /*
         * Basically figure out where the offsets are
         * Since canvas resides two divs down, you need to determine the offsets from each
         * Add them up and you have the approximate position of the canvas
         *
         * To figure out the scale, you figure out how much it has deviated from the original
         * size.
         * */
        var canvasScale = canvasObject.width/canvasObject.offsetWidth;
        $log.debug(canvasScale + " " + canvasObject.width + " " + canvasObject.offsetWidth);

        canvasOffsets.scale = canvasScale;
    }

    function getOffsets(canvasObject) {
        $log.debug("parent parent offsets: " + canvasObject.offsetParent.offsetParent.offsetLeft + " " +
            canvasObject.offsetParent.offsetParent.offsetTop);

        canvasOffsets.offsets = {
            x: canvasObject.offsetParent.offsetParent.offsetLeft +
            canvasObject.offsetParent.offsetLeft +
            canvasObject.offsetLeft,
            y: canvasObject.offsetParent.offsetParent.offsetTop +
            canvasObject.offsetParent.offsetTop +
            canvasObject.offsetTop
        };
    }

    function triggerMouseClick(e) {
        // http://stackoverflow.com/questions/28628964/mouse-position-within-html-5-responsive-canvas
        var mouseClick = parseMouseClick(e);

        if (addWaypoint(mouseClick)) {
            drawDot(mouseClick);
            drawFlightPath();
        }

        /*
        * Please note that if you need to delete a point you will need to redraw all the points
        * Since it stored as an array, could in theory, wipe then redraw
        * http://stackoverflow.com/questions/24140805/how-to-clear-specific-line-in-canvas-html5
        * */
    }

    function parseMouseClick(e) {
        $log.debug("x: " + e.x + " y: " + e.y);

        var scale = canvasOffsets.scale;
        var offsetX = canvasOffsets.offsets.x;
        var offsetY = canvasOffsets.offsets.y;

        var actualX = (e.x - offsetX) * scale;
        var actualY = (e.y - offsetY) * scale;

        $log.debug("actual x: " + actualX + " actual y: " + actualY);
        return {
            x: actualX,
            y: actualY
        };
    }

    function addWaypoint(mouseClick) {
        if (!matchesPreviousWaypoint(mouseClick)) {
            $scope.currentWaypoints.push(mouseClick);
            return true;
        }
        return false;
    }

    function matchesPreviousWaypoint(mouseClick) {
        if ($scope.currentWaypoints.length > 1) {
            var lastWaypoint = $scope.currentWaypoints[$scope.currentWaypoints.length - 1];
            //var matchesLastWaypoint = (lastWaypoint.x === mouseClick.x) && (lastWaypoint.y === mouseClick.y);
            //$log.debug("Does this click match last waypoint: " + matchesLastWaypoint);
            return (lastWaypoint.x === mouseClick.x) && (lastWaypoint.y === mouseClick.y);
        }
        return false;
    }

    function drawDot(mouseClick) {
        globalCanvasGrid.beginPath();
        globalCanvasGrid.arc(mouseClick.x, mouseClick.y, 2, 0, 2 * Math.PI, true);
        globalCanvasGrid.fill();
    }

    /*
    * Ideally this function should only be called once
    * */
    function drawFlightPath() {
        // Using the waypoints array join each one together
        var currentWaypoints = $scope.currentWaypoints;
        if (currentWaypoints.length > 1) {
            $log.debug("Drawing flight path now");
            var currentWaypoint = currentWaypoints[currentWaypoints.length - 2];
            var nextWaypoint = currentWaypoints[currentWaypoints.length - 1];
            globalCanvasGrid.moveTo(currentWaypoint.x, currentWaypoint.y);
            globalCanvasGrid.lineTo(nextWaypoint.x, nextWaypoint.y);
            globalCanvasGrid.stroke();
        }
    }

    /*
    * Final submission to the server
    * */

    $scope.submitMission = function () {
        var selectedDrone = $scope.selectedDrone;

        if (selectedDrone == undefined ||
            selectedDrone == null)
            $log.debug("An undefined selectedDrone");
        else {
            $log.debug($scope.selectedDrone.id);
            $log.debug("Mission has been started");

            var currentMission = {
                selectedDrone: selectedDrone.id,
                waypoints: $scope.currentWaypoints,
                altitude: 1,
                obstacles: [],
                pointOfInterest: {"x": 1, "y": 1}
            };

            var url = $scope.baseurl + "/rest/missions";
            $log.debug(currentMission);

            var request = {
                //url: url,
                //method: 'POST',
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE',
                    'Access-Control-Max-Age': '3600',
                    'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
                    'Content-Type': 'application/text',
                    'Access-Control-Allow-Credentials': false
                },
                data: currentMission
            };

            var config = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE',
                'Access-Control-Max-Age': '3600',
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
                'Content-Type': 'application/text',
                'Access-Control-Allow-Credentials': false
            };

            //$log.debug(request);

            /*$http.post(
                url,
                currentMission, function(data) {
                $log.debug(data);
                $log.debug(typeof(data));
            });*/
            $http.post(url, currentMission, config).then(function(data) {
                $log.debug(data);
                $log.debug(typeof(data));
            });
        }

    };
});