/**
 * Created by Joseph Tran on 29/10/2016.
 * This is a helpful REST API
 * https://thinkster.io/django-angularjs-tutorial
 *
 * AngularJS tutorial
 * https://www.toptal.com/angular-js/a-step-by-step-guide-to-your-first-angularjs-app
 */

var webServer = angular.module("webServer", [])
.controller("missionExecutionCtrl", function($log, $http, $interval, $scope)
{
    /* DEFAULT scope bindings */
    $scope.baseurl = "http://localhost:5001/rest/";
    var RESTMISSIONS = "missions";
    var RESTDRONES = "drones";
    var RESTIMAGES = "images";
    var RESTCURRENTIMAGE = "images/current";

    var INPROGRESS = "IN_PROGRESS";

    $scope.currentImage = "";
    $scope.currentMission = "";

    $scope.errorMsg = {
        heading: "ERROR",
        message: []
    };

    $scope.warningMsg = {
        heading: "Warning",
        message: []
    };

    $scope.successMsg = {
        heading: "Success",
        message: []
    };

    var config = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE',
        'Access-Control-Max-Age': '3600',
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
        'Content-Type': 'application/text',
        'Access-Control-Allow-Credentials': false
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
        window.location.href = "../index.html"
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

    function showWarningScreen (){
        jQuery(".loading").hide();
        jQuery(".warning").show();
    }

    $scope.closeWarningScreen = function (){
        jQuery(".warning").hide();
        $scope.warningMsg.message = [];
    };

    function addWarningMessage(message) {
        $scope.warningMsg.message.push(message);
    }

    function drawUpGrid(mission) {
        // TODO get current mission
        // TODO get canvas grid
        //var gridContext = jQuery("#mission-" + mission.mission.id)[0].getContext("2d");
        $log.debug(gridContext);
        drawHorizontalLines(gridContext);
        drawVerticalLines(gridContext);
        drawFlightPath(gridContext, mission.waypoints);
        drawDot(mission.point_of_interest, gridContext, ORANGE);
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

    /* FINISHED DEFAULT BINDINGS */

    $scope.init = function() {
        checkForCurrentMission();
    };

    var delayedMissionPoll = null;

    function checkForCurrentMission() {
        toggleLoadingScreen();
        $http.get($scope.baseurl + RESTMISSIONS)
            .then(function (data) {
                //$log.debug(data);
                toggleLoadingScreen();
                if (hasInProgressMission(data.data)) {
                    $scope.currentMission = getCurrentMission(data.data);
                    delayedMissionPoll = $interval(pollCurrentMission, 5000);
                }
                else {
                    addErrorMessage("No missions are running.");
                    showErrorScreen();
                }
            })
            .catch(function (data) {
                $log.error(data);
                addErrorMessage(data);
                showErrorScreen();
            });
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
            if(missions[i].mission.status === INPROGRESS)
                return missions[i];
        }
        return null;
    }

    function pollCurrentMission () {

        $http.get($scope.baseurl + RESTMISSIONS + "/" + $scope.currentMission.mission.id + "/status")
            .then(function (data) {
                $log.debug(data.data);
                if (data.data.status !== "IN PROGRESS") {
                    addErrorMessage("Mission is no longer running");
                    showErrorScreen();
                    $interval.cancel(delayedMissionPoll);
                    $scope.currentMission.mission.status = data.data.status;
                    $log.debug($scope.currentMission.mission.status);
                }
            })
            .catch(function(data) {
                $log.error("failed to poll");
                addErrorMessage(data);
                showErrorScreen();
            });
    }

    function pollCurrentImage() {

        $http.get($scope.baseurl + RESTCURRENTIMAGE)
            .then(function (data) {
                $log.debug(data.data);
                $scope.currentImage = data.data.imageblob;
            })
            .catch(function(data) {
                $log.error("failed to poll");
                addErrorMessage(data);
                showErrorScreen();
            });
    }

    // Look up interval angular
});
