/**
 * Created by Joseph Tran on 27/10/2016.
 */

angular.module("webServer")
.controller("missionStarterCtrl", function($log, $scope, restService) {
    $scope.missions = [];
    $scope.errorMsg = {
        heading: "ERROR",
        message: [],
        buttonMsg: "OK"
    };

    $scope.showCanvas = true;

    var RESTMISSION = "missions";

    var MINGRID = 0;
    var MAXGRID = 300;
    var INCREMENT = 50;
    var ORANGE = "#ff8900";

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

    $scope.loadMission = function () {
        window.location.href = "mission-executor.html";
    };

    function showSuccessScreen (){
        jQuery(".loading").hide();
        jQuery(".success").show();
    }

    $scope.closeSuccessScreen = function (){
        jQuery(".success").hide();
    };

    function addErrorMessage(message) {
        $scope.errorMsg.message.push(message);
    }

    function showMissionListing() {
        jQuery("#mission-listing").show();
    }

    $scope.init = function () {
        getAllMission();
    };

    function getAllMission() {
        toggleLoadingScreen();
        restService.get(RESTMISSION)
            .then(function(data) {
                $log.debug(data.data);
                toggleLoadingScreen();
                //showSuccessScreen();
                var i = 0;
                for (i = 0; i < data.data.length; i++) {
                    loadUpMission(data.data[i]);
                }
                showMissionListing();
            })
            .catch(function(data) {
                $scope.errorMsg.buttonMsg = "Return Home";
                displayError(data);
            });
    }

    function displayError(data) {
        addErrorMessage("Failed to send GET request");
        addErrorMessage(data);
        $log.debug(data);
        toggleLoadingScreen();
        showErrorScreen();
    }

    function loadUpMission(mission) {
        mission.waypoints = sanitizeWaypoints(mission.waypoints);
        mission.point_of_interest = sanitizePoint(mission.point_of_interest);
        $log.debug(mission.waypoints);
        $scope.missions.push(mission);
        $log.debug(mission.mission.id);
    }

    function drawUpGrid(mission) {
        var gridContext = jQuery("#mission-" + mission.mission.id)[0].getContext("2d");
        $log.debug(gridContext);
        drawHorizontalLines(gridContext);
        drawVerticalLines(gridContext);
        drawFlightPath(gridContext, mission.waypoints);
        drawDot(mission.point_of_interest, gridContext, ORANGE);
    }

    $scope.startMission = function(missionId) {
        $log.debug("Trying to start missiong with id: " + missionId);
        restService.get(RESTMISSION + "/" + missionId + "/start")
            .then(function() {
                showSuccessScreen();
            })
            .catch(function(data) {
                displayError(data);
            });
    };

    $scope.$on("onLastRepeatItem", function (scope, element, attrs) {
        var i = 0;
        for (i = 0; i < $scope.missions.length; i++) {
            var mission = $scope.missions[i];
            drawUpGrid(mission);
        }
    });

    $scope.createAMission = function () {
        window.location.href = "mission-creator.html"
    };

    /*Code from Mission Controller*/
    function drawDot(mouseClick, canvasGrid, colour) {
        canvasGrid.beginPath();
        canvasGrid.arc(mouseClick.x, mouseClick.y, 2, 0, 2 * Math.PI, true);
        if (exists(colour)) {
            canvasGrid.fillStyle = colour;
        }
        canvasGrid.fill();
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

    /*This is slightly modified from controller*/
    function drawFlightPath(flightPathGrid, waypoints, colour) {
        // Using the waypoints array join each one together

        if (waypoints.length > 1) {
            $log.debug("Drawing flight path now");
            for (var i = 0; i < waypoints.length - 1; i++) {
                var currentWaypoint = waypoints[i];
                drawDot(currentWaypoint, flightPathGrid);
                var nextWaypoint = waypoints[i + 1];
                drawDot(nextWaypoint, flightPathGrid);
                flightPathGrid.moveTo(currentWaypoint.x, currentWaypoint.y);
                flightPathGrid.lineTo(nextWaypoint.x, nextWaypoint.y);
                if (exists(colour)) {
                    flightPathGrid.strokeStyle = colour;
                }
                flightPathGrid.stroke();
            }
        }
    }

    function exists(object) {
        return (object !== undefined) &&
            (object !== null);
    }

    function sanitizeWaypoints(array) {
        var sanitizedArray = [];
        for(var i = 0; i < array.length; i++) {
            sanitizedArray.push(sanitizePoint(array[i]));
        }
        return sanitizedArray;
    }

    function sanitizePoint(point) {
        $log.debug(point);
        point.x = point.x + 150;
        point.y = (point.y * -1) + 150;
        $log.debug(point);
        return point;
    }
});

webServer.directive("onLastRepeatItem", function () {
    return function(scope, element, attrs){
        if (scope.$last) {
            setTimeout(function () {
                scope.$emit("onLastRepeatItem", element, attrs)
            }, 1);
        }
    }
});

webServer.config(function ($logProvider) {
    $logProvider.debugEnabled(false);
});