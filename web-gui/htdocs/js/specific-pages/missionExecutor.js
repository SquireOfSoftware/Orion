/**
 * Created by Joseph Tran on 29/10/2016.
 * This is a helpful REST API
 * https://thinkster.io/django-angularjs-tutorial
 *
 * AngularJS tutorial
 * https://www.toptal.com/angular-js/a-step-by-step-guide-to-your-first-angularjs-app
 */

angular.module("webServer")
.controller("missionExecutionCtrl", function($log, $http, $interval, $scope)
{
    /* DEFAULT scope bindings */
    $scope.baseurl = "http://localhost:5001/rest/";
    var RESTMISSIONS = "missions";
    var RESTDRONES = "drones";
    var RESTCURRENTIMAGE = "images/current";

    var INPROGRESS = "IN PROGRESS";
    var COMPLETED = "COMPLETED";

    $scope.currentImage = "";
    $scope.currentMission = "";
    $scope.currentMetadataDump = {};

    var timeoutCounter = 0;

    $scope.errorMsg = {
        heading: "ERROR",
        message: [],
        buttonMsg: "OK"
    };

    $scope.warningMsg = {
        heading: "Warning",
        message: []
    };

    $scope.successMsg = {
        heading: "Success",
        message: []
    };

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

    function addErrorMessage(message) {
        $scope.errorMsg.message.push(message);
    }

    function showSuccessScreen (){
        jQuery(".loading").hide();
        jQuery(".success").show();
    }

    $scope.closeSuccessScreen = function (){
        jQuery(".success").hide();
    };

    function addSuccessMessage(message) {
        $scope.successMsg.message.push(message);
    }

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

    function drawUpGrid() {
        var gridContext = jQuery("#mission-grid")[0].getContext("2d");
        $log.debug(gridContext);
        drawHorizontalLines(gridContext);
        drawVerticalLines(gridContext);
        drawFlightPath(gridContext, $scope.currentMission.waypoints);
        drawDot($scope.currentMission.point_of_interest, gridContext, ORANGE);
    }

    /* FINISHED DEFAULT BINDINGS */

    function addErrorReturnButton(message) {
        $scope.errorMsg.buttonMsg = message;
    }

    $scope.init = function() {
        checkForCurrentMission();
    };

    var delayedMissionPoll = null;
    $scope.showCanvas = false;
    $scope.showMission = true;
    $scope.showImage = true;
    $scope.showDrone = true;

    function checkForCurrentMission() {
        toggleLoadingScreen();
        $http.get($scope.baseurl + RESTMISSIONS)
            .then(function (data) {
                //$log.debug(data);
                toggleLoadingScreen();
                if (hasInProgressMission(data.data)) {
                    $scope.currentMission = getCurrentMission(data.data);
                    delayedMissionPoll = $interval(pollCurrentMission, 5000);
                    showCurrentMissionScreen();
                    setTimeout(function () {drawUpGrid();}, 1);
                }
                else {
                    addErrorMessage("No missions are running.");
                    addErrorReturnButton("Return Home");
                    showErrorScreen();
                }
            })
            .catch(function (data) {
                $log.error(data);
                addErrorReturnButton("Return Home");
                addErrorMessage(data);
                showErrorScreen();
            });
    }

    function showCurrentMissionScreen() {
        jQuery(".current-mission").show();
    }

    function hasInProgressMission(missions) {
        for (var i = 0; i < missions.length; i++) {
            $log.debug(missions[i].mission.status);
            if(missions[i].mission.status === INPROGRESS) {
                return true;
            }
        }
        return false;
    }

    function getCurrentMission(missions) {
        for (var i = 0; i < missions.length; i++) {
            if(missions[i].mission.status === INPROGRESS) {
                missions[i].waypoints = sanitizeWaypoints(missions[i].waypoints);
                missions[i].point_of_interest = sanitizePoint(missions[i].point_of_interest);
                return missions[i];
            }
        }
        return null;
    }

    function pollCurrentMission () {
        pollCurrentMissionStatus();
        pollCurrentImage();
        pollCurrentDroneStatus();
        pollCurrentDroneMetadata();
        if (timeoutCounter > 1) {
            $scope.closeErrorScreen();
            addErrorMessage("Lost connection to server");
            showErrorScreen();
            stopPoll();
            timeoutCounter = 0;
        }
    }

    function pollCurrentMissionStatus() {
        $http.get($scope.baseurl + RESTMISSIONS + "/" + $scope.currentMission.mission.id + "/status")
            .then(function (data) {
                $log.debug(data.data);
                var status = data.data.status;
                if (status !== INPROGRESS) {
                    addErrorMessage("Mission is no longer running");
                    if (status === COMPLETED) {
                        addSuccessMessage("Mission completed");
                        showSuccessScreen();
                    }
                    else {
                        showErrorScreen();
                    }
                    stopPoll();
                    $scope.currentMission.mission.status = status;
                    $log.debug($scope.currentMission.mission.status);
                }
                timeoutCounter = 0;
            })
            .catch(function(data) {
                $log.error("failed to poll");
                timeoutCounter += 1;
            });
    }

    var IMAGEHEADER = "data:image/png;base64,";

    function pollCurrentImage() {
        $http.get($scope.baseurl + RESTCURRENTIMAGE)
            .then(function (data) {
                $log.debug(data.data);
                $scope.currentImage = IMAGEHEADER + data.data.imageblob;
                timeoutCounter = 0;
            })
            .catch(function(data) {
                $log.error("failed to poll");
                timeoutCounter += 1;
            });
    }

    function pollCurrentDroneStatus() {
        $http.get($scope.baseurl + RESTDRONES + "/" + $scope.currentMission.mission.drone_id + "/status")
            .then(function (data) {
                $log.debug(data.data.status);
                var status = data.data.status;
                $scope.currentMission.mission.drone_status = status;
                timeoutCounter = 0;
            })
            .catch(function (data) {
                $log.error(data);
                timeoutCounter += 1;
            })
    }

    function pollCurrentDroneMetadata() {
        $http.get($scope.baseurl + RESTDRONES + "/" + $scope.currentMission.mission.drone_id + "/metadata/current")
            .then(function (data) {
                $log.debug(data.data);
                $scope.currentMetadataDump = data.data;
            })
            .catch(function (data) {
                $log.error(data);
                timeoutCounter += 1;
            })
    }

    function stopPoll() {
        $interval.cancel(delayedMissionPoll);
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

webServer.config(function ($logProvider) {
    $logProvider.debugEnabled(false);
});