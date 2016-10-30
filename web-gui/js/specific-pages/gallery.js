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
        loadImages(0, 5);
    };

    /* always assume start and end are always numbers and are legit*/
    function loadImages(start_number, end_number) {
        toggleLoadingScreen();
        var url = $scope.baseurl + RESTIMAGES +
            "?start_number=" + start_number +
            "&end_number" + end_number;
        $http.get(url)
            .then(function(data) {
                toggleLoadingScreen();
                $log.debug(data.data);
                $scope.images = data.data;
            })
            .catch(function(data) {
                $log.error(data);
                addErrorMessage(data);
                showErrorScreen();
            })
    }
});