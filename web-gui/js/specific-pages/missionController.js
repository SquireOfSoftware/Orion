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

    $scope.altitude = 50;

    var MINGRID = 0;
    var MAXGRID = 300;

    var flightPathCanvasGrid = null;
    var canvasOffsets = {};
    $scope.currentWaypoints = [];
    $scope.currentPointOfInterest = {};

    $scope.canSubmitMission = false;

    $scope.init = function() {
        $(".mission-page").hide();
        $("#select-a-drone-page").show();
        initialiseDrones();
    };

    /*
    * This is for the first screen
    * */

    function initialiseDrones() {
        addDrone(setupDrone("2", "Voyager", "../../images/Drone1.png"));
        addDrone(setupDrone("1", "Sputnik", "../../images/Drone2.png"));
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

    $scope.showFlightPath = function () {
        isValidMission();
        jQuery("#select-a-drone-page").hide();
        jQuery("#canvas-point-of-interest").hide();
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
        var canvasGrid = jQuery("#canvas-grid")[0].getContext('2d');
        canvasGrid = drawVerticalLines(canvasGrid);
        canvasGrid = drawHorizontalLines(canvasGrid);
        flightPathCanvasGrid = canvasGrid;
        initialiseFlightPathGrid();
    }

    function initialiseFlightPathGrid() {
        var canvasObject = jQuery("#canvas-flight-path")[0];
        canvasObject.addEventListener("mousedown", triggerMouseClick, false);

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

    /*
    * TODO PLEASE FIX THIS FOR FIREFOX, SINCE THIS ONLY WORKS FOR CHROME
    * */
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
        var canvasObject = jQuery("#canvas-grid")[0];
        getScale(canvasObject);
        getOffsets(canvasObject);

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

    /*
    * This needs to be cross browser supported
    * http://www.quirksmode.org/mobile/viewports2.html
    * */
    function parseMouseClick(e) {

        var x = e.pageX;
        var y = e.pageY;

        $log.debug("x: " + x + " y: " + y);

        var scale = canvasOffsets.scale;
        var offsetX = canvasOffsets.offsets.x;
        var offsetY = canvasOffsets.offsets.y;

        var actualX = (x - offsetX) * scale;
        var actualY = (y - offsetY) * scale;

        $log.debug("offset x:" + offsetX + " offset y:" + offsetY);

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
        flightPathCanvasGrid.beginPath();
        flightPathCanvasGrid.arc(mouseClick.x, mouseClick.y, 2, 0, 2 * Math.PI, true);
        flightPathCanvasGrid.fill();
    }

    /*
    * Ideally this function should only be called once per click
    * */
    function drawFlightPath() {
        // Using the waypoints array join each one together
        var currentWaypoints = $scope.currentWaypoints;
        if (currentWaypoints.length > 1) {
            $log.debug("Drawing flight path now");
            var currentWaypoint = currentWaypoints[currentWaypoints.length - 2];
            var nextWaypoint = currentWaypoints[currentWaypoints.length - 1];
            flightPathCanvasGrid.moveTo(currentWaypoint.x, currentWaypoint.y);
            flightPathCanvasGrid.lineTo(nextWaypoint.x, nextWaypoint.y);
            flightPathCanvasGrid.stroke();
        }
    }

    /*
    * Point of interest
    * */
    $scope.showPointOfInterest = function() {
        flightPathCanvasActive = false;
        // Need proper architecture after this is resolved.
        jQuery("#canvas-flight-path").hide();
        var canvasObject = jQuery("#canvas-point-of-interest")[0];
        jQuery("#canvas-point-of-interest").show();
        canvasObject.addEventListener("mousedown", selectPointOfInterest, false);
        isValidMission();
    };

    function selectPointOfInterest(e) {
        var canvasObject = jQuery("#canvas-grid")[0];
        getScale(canvasObject);
        getOffsets(canvasObject);

        var mouseClick = parseMouseClick(e);
        $scope.currentPointOfInterest = mouseClick;
    }

    /*
    * Final submission to the server
    * */

    function isValidMission () {
        var currentMission = $scope.currentMission;
        var isValid = hasDrone(currentMission.selectedDrone) &&
                hasWaypoints(currentMission.waypoints) &&
                hasAltitude(currentMission.altitude) &&
                hasPointOfInterest(currentMission.pointOfInterest);
        $log.debug(isValid);
        $scope.canSubmitMission = isValid;
    }

    function hasDrone(selectedDrone) {
        return (exists(selectedDrone));
    }

    function hasWaypoints(waypoints) {
        return (exists(waypoints)) &&
            (waypoints.length > 0);
    }

    function hasAltitude(altitude) {
        return (exists(altitude)) &&
            (altitude > 0) &&
            (altitude < 300);
    }

    function hasPointOfInterest(pointOfInterest) {
        return (exists(pointOfInterest));
    }

    function exists(object) {
        return (object !== undefined) &&
            (object !== null);
    }

    $scope.submitMission = function () {
        var selectedDrone = $scope.selectedDrone;

        if (selectedDrone == undefined ||
            selectedDrone == null)
            $log.debug("An undefined selectedDrone");
        else {
            $log.debug($scope.selectedDrone.id);
            $log.debug("Mission has been started");

            var currentMission = {
                selectedDrone: selectedDrone,
                waypoints: $scope.currentWaypoints,
                altitude: $scope.altitude,
                obstacles: [],
                pointOfInterest: $scope.currentPointOfInterest
            };

            var url = $scope.baseurl + "/rest/missions";
            $log.debug(currentMission);

            // How to bypass CORS on mac
            // open -a Google\ Chrome --args --disable-web-security --user-data-dir

            var config = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE',
                'Access-Control-Max-Age': '3600',
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
                'Content-Type': 'application/text',
                'Access-Control-Allow-Credentials': false
            };

            $http.post(url, currentMission, config).then(function(data) {
                $log.debug(data);
                $log.debug(typeof(data));
            });
        }

    };
});