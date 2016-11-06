/**
 * Created by Joseph Tran on 30/10/2016.
 */

angular.module("webServer")
.controller("galleryCtrl", function($log, $scope, restService) {
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

    function exists(object) {
        return (object !== undefined) &&
            (object !== null);
    }

    /* FINISHED DEFAULT BINDINGS */

    $scope.init = function() {
        loadCurrentImage();
    };

    function loadCurrentImage() {
        toggleLoadingScreen();
        restService.get(RESTCURRENTIMAGE)
            .then(function (data) {
                toggleLoadingScreen();
                $log.debug(data.data);
                addPreviousImage(data.data);
                $scope.currentImage = data.data;
                jQuery(".onload").show();
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

    function loadImagesById(lastImageID) {
        toggleLoadingScreen();
        var imageNumber = 10;
        $log.debug(RESTIMAGES + "/" + lastImageID + "/filter?length=" + imageNumber);
        restService.get(url)
            .then(function (data) {
                $log.debug(data.data);
                if (exists(data.data))
                    for (var i = 0; i < data.data.length; i++) {
                        addImage(data.data[i]);
                        $log.debug("image id: " + data.data[i].id);
                    }
                toggleLoadingScreen();
            })
            .catch(function (data) {
                $log.error(data);
                addErrorMessage(data);
                showErrorScreen();
            });
    }

    function addImage(image) {
        $scope.images.push(image);
        if (doesNotMatchEntries(image.mission_id)) {
            $scope.missions.push(image.mission_id);
        }
    }

    function addPreviousImage(image) {
        $scope.images.unshift(image);
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
        return ($scope.selectedMission === null) ||
            (missionID === $scope.selectedMission) ||
            ($scope.selectedMission === "ALL");
    };

    $scope.selectImage = function(image) {
        $scope.currentImage = image;
    }
});

webServer.config(function ($logProvider) {
    //$logProvider.debugEnabled(false);
});