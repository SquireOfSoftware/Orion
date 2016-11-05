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
    $scope.baseurl = "http://localhost:5001/rest/";
    var RESTMISSIONS = "missions";
    var RESTDRONES = "drones";
    $scope.errorMsg = {
        heading: "ERROR",
        message: [],
        buttonMsg: "OK"
    };

    var config = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE',
        'Access-Control-Max-Age': '3600',
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
        'Content-Type': 'application/text',
        'Access-Control-Allow-Credentials': false
    };

    // Mission variables

    $scope.currentMission = {};

    $scope.selectedDrone = null;
    $scope.altitude = 50;

    $scope.currentWaypoints = [];
    $scope.currentPointOfInterest = {};

    var MINGRID = 0;
    var MAXGRID = 300;
    var INCREMENT = 50;
    var MINALT = 0;
    var MAXALT = 250;

    var ORANGE = "#ff8900";
    var GREY = "#E0E0E0";

    // Grids
    var interactionGridContext = null;
    var pointOfInterestGridContext = null;
    var flightPathGridContext = null;
    var baseGridContext = null;

    var SCREENS = {
        flightPath: 1,
        pointOfInterest: 2
    };
    var currentScreenState = -1;

    $scope.init = function() {
        initialiseDrones();
        initialiseGrids();
    };

    /*
    * This is for the first screen
    * */

    function initialiseDrones() {
        toggleLoadingScreen();
        $http.get($scope.baseurl + RESTDRONES)
            .then(function(data) {
                $log.debug(data.data);
                $scope.drones = data.data;
                if (data.data.length > 0) {
                    $scope.selectedDrone = data.data[0];
                }
                toggleLoadingScreen();
            })
            .catch(function(data) {
                toggleLoadingScreen();
                $scope.errorMsg.buttonMsg = "Return Home";
                addErrorMessage("Cannot load drones");
                addErrorMessage(data);
                showErrorScreen();
                $log.error("Cannot load drones");
                $log.error(data);
            })
    }

    /*
    * This is for the grid screen
    * */

    function initialiseGrids() {
        initialiseBaseGrid(jQuery("#canvas-grid")[0]);
        initialiseFlightPathGrid(jQuery("#canvas-flight-path")[0]);
        initialisePointOfInterestGrid(jQuery("#canvas-point-of-interest")[0]);
        initialiseInteractionGrid(jQuery("#canvas-interaction")[0]);
        currentScreenState = SCREENS.flightPath;
    }

    function getContextFromGrid(canvasObject) {
        return canvasObject.getContext("2d");
    }

    function initialiseBaseGrid(canvasGridObject) {
        baseGridContext = getContextFromGrid(canvasGridObject);
        drawVerticalLines(baseGridContext);
        drawHorizontalLines(baseGridContext);
    }

    function initialiseInteractionGrid(canvasGridObject) {
        $log.debug("Linking the mouse");
        interactionGridContext = canvasGridObject.getContext("2d");
        canvasGridObject.addEventListener("mousedown", triggerMouseClick, false);
    }

    function initialiseFlightPathGrid(canvasGridObject) {
        flightPathGridContext = getContextFromGrid(canvasGridObject);
        $log.debug(flightPathGridContext);
    }

    function initialisePointOfInterestGrid(canvasGridObject) {
        pointOfInterestGridContext = getContextFromGrid(canvasGridObject);
    }

    function drawVerticalLines(canvasGrid) {
        for (var x = MINGRID; x <= MAXGRID; x += INCREMENT) {
            canvasGrid.moveTo(x, MINGRID);
            canvasGrid.lineTo(x, MAXGRID);
            canvasGrid.fillStyle = GREY;
            canvasGrid.stroke();
        }
    }

    function drawHorizontalLines(canvasGrid) {
        for (var y = MINGRID; y <= MAXGRID; y += INCREMENT) {
            canvasGrid.moveTo(MINGRID, y);
            canvasGrid.lineTo(MAXGRID, y);
            canvasGrid.fillStyle = GREY;
            canvasGrid.stroke();
        }
    }

    function setupScaleAndOffsets() {
        var canvasObject = jQuery("#canvas-grid")[0];
        return {
            scale: getScale(canvasObject),
            offsets: getOffsets(canvasObject)
        };
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
        return canvasScale;
    }

    function getOffsets(canvasObject) {
        $log.debug("parent parent offsets: " + canvasObject.offsetParent.offsetParent.offsetLeft + " " +
            canvasObject.offsetParent.offsetParent.offsetTop);

        return {
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
        $log.debug("Mouse click!!");

        var scaleAndOffsets = setupScaleAndOffsets();

        var mouseClick = parseMouseClick(e, scaleAndOffsets);
        if (isMouseClickValid(mouseClick)) {
            switch (currentScreenState) {
                //var flightPathGridContext = getContextFromGrid(jQuery("#canvas-flight-path")[0]);
                case SCREENS.flightPath:
                    if (addWaypoint(mouseClick)) {
                        drawDot(mouseClick, flightPathGridContext);
                        drawFlightPath(flightPathGridContext);
                    }
                    break;
                case SCREENS.pointOfInterest:
                    $log.debug(pointOfInterestGridContext);
                    clearGrid(pointOfInterestGridContext);
                    drawDot(mouseClick, pointOfInterestGridContext, ORANGE);
                    $scope.currentPointOfInterest = mouseClick;
                    break;
                default:
                    $log.error("I dont recognise this screen");
            }
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
    function parseMouseClick(e, scaleAndOffsets) {

        var x = e.pageX;
        var y = e.pageY;

        $log.debug("x: " + x + " y: " + y);

        var scale = scaleAndOffsets.scale;
        var offsetX = scaleAndOffsets.offsets.x;
        var offsetY = scaleAndOffsets.offsets.y;

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
            return (lastWaypoint.x === mouseClick.x) && (lastWaypoint.y === mouseClick.y);
        }
        return false;
    }

    function drawDot(mouseClick, canvasGrid, colour) {
        canvasGrid.beginPath();
        canvasGrid.arc(mouseClick.x, mouseClick.y, 2, 0, 2 * Math.PI, true);
        if (exists(colour)) {
            canvasGrid.fillStyle = colour;
        }
        canvasGrid.fill();
    }

    function clearGrid(contextObject) {
        var canvasObject = contextObject.canvas;
        $log.debug("Clearing grid: ");
        $log.debug(contextObject);
        contextObject.clearRect(0, 0, canvasObject.width, canvasObject.height);
    }

    function isMouseClickValid(mouseClick) {
        return (mouseClick.x >= MINGRID) &&
            (mouseClick.x <= MAXGRID) &&
            (mouseClick.y >= MINGRID) &&
            (mouseClick.y <= MAXGRID);
    }

    /*
    * Ideally this function should only be called once per click
    * */
    function drawFlightPath(flightPathGrid, colour) {
        // Using the waypoints array join each one together
        var currentWaypoints = $scope.currentWaypoints;
        if (currentWaypoints.length > 1) {
            $log.debug("Drawing flight path now");
            var currentWaypoint = currentWaypoints[currentWaypoints.length - 2];
            var nextWaypoint = currentWaypoints[currentWaypoints.length - 1];
            flightPathGrid.moveTo(currentWaypoint.x, currentWaypoint.y);
            flightPathGrid.lineTo(nextWaypoint.x, nextWaypoint.y);
            if (exists(colour)) {
                flightPathGrid.strokeStyle = colour;
            }
            flightPathGrid.stroke();
        }
    }

    /*
    * Point of interest
    * */

    $scope.switchToPointOfInterest = function () {
        currentScreenState = SCREENS.pointOfInterest;
    };

    $scope.switchToFlightPath = function () {
        currentScreenState = SCREENS.flightPath;
    };

    $scope.clearPointOfInterest = function () {
        $scope.currentPointOfInterest = {};
        clearGrid(pointOfInterestGridContext);
    };

    $scope.clearFlightPath = function () {
        $scope.currentWaypoints = [];
        clearGrid(flightPathGridContext);
    };

    /*
    * Final submission to the server
    * */

    function isValidMission (currentMission) {
        var isValid = hasDrone(currentMission.selectedDrone) &&
                hasWaypoints(currentMission.waypoints) &&
                hasAltitude(currentMission.altitude) &&
                hasPointOfInterest(currentMission.pointOfInterest);
        $log.debug("Is mission valid? " + isValid);
        return isValid;
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
            (altitude > MINALT) &&
            (altitude < MAXALT);
    }

    function hasPointOfInterest(pointOfInterest) {
        return (exists(pointOfInterest) &&
            (exists(pointOfInterest.x)) &&
            (exists(pointOfInterest.y)));
    }

    function exists(object) {
        return (object !== undefined) &&
            (object !== null);
    }

    function toggleLoadingScreen() {
        jQuery(".loading").toggle();
    }

    function showErrorScreen() {
        jQuery(".loading").hide();
        jQuery(".errors").show();
    }

    $scope.closeErrorScreen = function () {
        jQuery(".errors").hide();
        $scope.errorMsg.message = [];
        if ($scope.errorMsg.buttonMsg !== "OK") {
            window.location.href = "../index.html";
        }
    };

    $scope.loadMissionScreen = function () {
        window.location.href = "mission-starter.html";
    };

    function showSuccessScreen (){
        jQuery(".loading").hide();
        jQuery(".success").show();
    };

    function addErrorMessage(message) {
        $scope.errorMsg.message.push(message);
    }

    $scope.submitMission = function () {
        toggleLoadingScreen();
        var selectedDrone = $scope.selectedDrone;

        if (exists(selectedDrone)) {
            $log.debug($scope.selectedDrone.id);

            var currentMission = {
                selectedDrone: selectedDrone,
                waypoints: sanitizeWaypoints($scope.currentWaypoints),
                altitude: $scope.altitude,
                obstacles: [],
                pointOfInterest: sanitizePoint($scope.currentPointOfInterest)
            };

            sendMission(currentMission);
        }
    };

    function sanitizeWaypoints(array) {
        var sanitizedArray = [];
        for(var i = 0; i < array.length; i++) {
            sanitizedArray.push(sanitizePoint(array[i]));
        }
        return sanitizedArray;
    }

    function sanitizePoint(point) {
        $log.debug(point);
        var sanitizedPoint = {
            x: point.x - 150,
            y: (point.y * -1) + 150
        };
        $log.debug(sanitizedPoint);
        return sanitizedPoint;
    }

    function sendMission(currentMission) {
        if (isValidMission(currentMission)) {
            var url = $scope.baseurl + RESTMISSIONS;
            $log.debug("trying to send mission");

            // How to bypass CORS on mac
            // open -a Google\ Chrome --args --disable-web-security --user-data-dir

            //showSuccessScreen();

            $http.post(url, currentMission, config).then(function (data) {
                toggleLoadingScreen();
                $log.debug(data);
                $log.debug(typeof(data));
                showSuccessScreen();
            })
            .catch(function (data) {
                $log.error(data);
                addErrorMessage("There was an error with your submission.");
                addErrorMessage(data.data.data);
                jQuery(".errors").show();
                showErrorScreen();
            });
        }
        else {
            addErrorMessage("The following are invalid:");
            if (!hasDrone(currentMission.selectedDrone))
                addErrorMessage("+ Drone must be selected");
            if (!hasWaypoints(currentMission.waypoints))
                addErrorMessage("+ Waypoints must be selected");
            if (!hasAltitude(currentMission.altitude))
                addErrorMessage("+ Altitude must be between 0 and 300cm");
            if (!hasPointOfInterest(currentMission.pointOfInterest))
                addErrorMessage("+ A point of interest must be selected");
            $log.debug(currentMission);
            showErrorScreen();
        }
    }
});

webServer.config(function ($logProvider) {
    $logProvider.debugEnabled(false);
});