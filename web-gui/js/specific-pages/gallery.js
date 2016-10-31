/**
 * Created by Joseph Tran on 30/10/2016.
 */

var webServer = angular.module("webServer", [])
.controller("galleryCtrl", function($log, $http, $scope) {
    $scope.baseurl = "http://localhost:5001/rest/";
    var RESTMISSIONS = "missions";
    var RESTDRONES = "drones";
    var RESTIMAGES = "images";
    var RESTCURRENTIMAGE = "images/current";

    $scope.errorMsg = {
        heading: "ERROR",
        message: [],
        buttonMsg: "OK"
    };

    $scope.missions = ["ALL"];
    $scope.selectedMission = "ALL";

    $scope.currentImage = "";

    $scope.images = [];

    /* DEFAULT bindings from every other page */

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

    function addErrorButtonMessage(message) {
        $scope.errorMsg.buttonMsg = message;
    }

    function exists(object) {
        return (object !== undefined) &&
            (object !== null);
    }

    /* FINISHED DEFAULT BINDINGS */

    $scope.init = function() {
        //loadAllMissions();
        loadImages(0, 5);
    };

    /* always assume start and end are always numbers and are legit*/
    function loadImages(start_number, end_number) {
        toggleLoadingScreen();
        var url = $scope.baseurl + RESTIMAGES +
            "?start_number=" + start_number +
            "&end_number=" + end_number;
        $http.get(url)
            .then(function(data) {
                toggleLoadingScreen();
                $log.debug(data.data);
                $scope.images = data.data;
                loadUpMissions(data.data);
            })
            .catch(function(data) {
                $log.error(data);
                addErrorMessage(data);
                showErrorScreen();
            })
    }

    function loadUpMissions(array){
        for(var i = 0; i < array.length; i++){
            $log.debug(array[i]);
            if (doesNotMatchEntries(array[i].mission_id))
                $scope.missions.push(array[i].mission_id);
        }
    }

    function doesNotMatchEntries(entry) {
        for(var i = 0; i < $scope.missions.length; i++) {
            if($scope.missions[i] === entry)
                return false;
        }
        return true;
    }

    function loadAllMissions() {
        toggleLoadingScreen();
        var url = $scope.baseurl + RESTMISSIONS;
        $http.get(url)
            .then(function(data) {
                toggleLoadingScreen();
                $log.debug(data.data);
                $scope.missions = data.data;
                $scope.missions.unshift({"mission": {"id": "ALL"}});
                $log.debug($scope.missions);
                if ($scope.missions.length > 0) {
                    $log.debug("setting the mission");
                    $scope.selectedMission = $scope.missions[0];
                }
            })
            .catch(function(data) {
                $log.error(data);
                addErrorMessage(data);
                showErrorScreen();
            })
    }

    $scope.showFilter = function(missionID) {
        return ($scope.selectedMission.mission.id === null) ||
            (missionID === $scope.selectedMission.mission.id) ||
            ($scope.selectedMission.mission.id === "ALL");
    };
});