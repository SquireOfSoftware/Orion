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
        loadCurrentImage();
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

    function loadCurrentImage() {
        toggleLoadingScreen();
        var url = $scope.baseurl + RESTIMAGES + "/current";
        $http.get(url)
            .then(function (data) {
                toggleLoadingScreen();
                $log.debug(data.data);
                addImage(data.data);
                $scope.currentImage = data.data;
            })
            .catch(function (data) {
                $log.error(data);
                addErrorMessage(data);
                showErrorScreen();
            });
    }

    $scope.loadMore = function() {
        var lastImageID = $scope.images[$scope.images.length - 1].id;
        if (exists(lastImageID))
            loadImagesById(lastImageID);
        else
            $log.error("There is an undefined id");
    };

    $scope.loadCurrent = function() {
        toggleLoadingScreen();
        var url = $scope.baseurl + RESTIMAGES + "/current";
        $http.get(url)
            .then(function (data) {
                toggleLoadingScreen();
                $log.debug(data.data);
                addImage(data.data);
                $scope.currentImage = data.data;
            })
            .catch(function (data) {
                $log.error(data);
                addErrorMessage(data);
                showErrorScreen();
            });
    };

    function loadImagesById(lastImageID) {
        toggleLoadingScreen();
        var imageNumber = 1;
        var url = $scope.baseurl + RESTIMAGES + "/" + lastImageID + "/filter?length=" + imageNumber;
        $http.get(url)
            .then(function (data) {
                //$log.debug(data.data[0]);
                if (exists(data.data))
                    for (var i = 0; i < data.data.length; i++) {
                        addImage(data.data[i]);
                    }
                toggleLoadingScreen();
            })
            .catch(function (data) {
                $log.error(data);
                addErrorMessage(data);
                showErrorScreen();
            });
    }

    function loadUpMissions(array){
        for(var i = 0; i < array.length; i++){
            if (doesNotMatchEntries(array[i].mission_id))
                $scope.missions.push(array[i].mission_id);
            $log.debug($scope.missions);
        }
    }

    function addImage(image) {
        $scope.images.push(image);
        if (doesNotMatchEntries(image.mission_id)) {
            $scope.missions.push(image.mission_id);
        }
    }

    function doesNotMatchEntries(entry) {
        for(var i = 0; i < $scope.missions.length; i++) {
            if($scope.missions[i] === entry)
                return false;
        }
        return true;
    }

    $scope.showFilter = function(missionID) {
        $log.debug(missionID);
        var show = ($scope.selectedMission === null) ||
            (missionID === $scope.selectedMission) ||
            ($scope.selectedMission === "ALL");
        //$log.debug(show);
        return show;
    };

    $scope.selectImage = function(image) {
        $scope.currentImage = image;
    }
});