/**
 * Created by Joseph Tran on 1/10/2016.
 * This is a helpful REST API
 * https://thinkster.io/django-angularjs-tutorial
 *
 * AngularJS tutorial
 * https://www.toptal.com/angular-js/a-step-by-step-guide-to-your-first-angularjs-app
 */

angular.module("webServer", [])
.controller("missionCtrl", function($log, $http, $scope)
{
    $scope.drones = [];
    $scope.baseurl = "http://localhost:5001";
    $scope.warningMsg = "";

    $scope.canSubmitMission = false;

    // Mission variables

    $scope.currentMission = {};

    $scope.selectedDrone = null;
    $scope.altitude = 50;

    $scope.currentWaypoints = [];
    $scope.currentPointOfInterest = {};

    var MINGRID = 0;
    var MAXGRID = 300;
    var INCREMENT = 50;

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
        initialiseDummyDrones();
        initialiseGrids();
    };

    /*
    * This is for the first screen
    * */

    function initialiseDummyDrones() {
        addDrone(setupDrone("2", "Voyager", "../../images/Drone1.png"));
        addDrone(setupDrone("1", "Sputnik", "../../images/Drone2.png"));
        $scope.selectedDrone = $scope.drones[0];
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
            canvasGrid.stroke();
        }
    }

    function drawHorizontalLines(canvasGrid) {
        for (var y = MINGRID; y <= MAXGRID; y += INCREMENT) {
            canvasGrid.moveTo(MINGRID, y);
            canvasGrid.lineTo(MAXGRID, y);
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
        switch(currentScreenState) {
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
                drawDot(mouseClick, pointOfInterestGridContext, "#ff8900");
                break;
            default:
                $log.error("I dont recognise this screen");
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
            //var matchesLastWaypoint = (lastWaypoint.x === mouseClick.x) && (lastWaypoint.y === mouseClick.y);
            //$log.debug("Does this click match last waypoint: " + matchesLastWaypoint);
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
                })
                .catch(function(data) {
                    $scope.warningMsg = "There was an error with your submission.";
                    jQuery(".errors")
                })
            ;
        }

    };
});