/**
 * Created by JarvisWalker on 27/10/2016.
 */

var webServer = angular.module("webServer", [])
.controller("missionStarterCtrl", function($log, $http, $scope) {
    $scope.missions = [];
    $scope.errorMsg = {
        heading: "ERROR",
        message: ""
    };

    var baseurl = "http://localhost:5001/rest/";
    var RESTMISSION = "missions";

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
    };

    $scope.loadMission = function () {
        // TODO this is to load the started mission
        jQuery(".loading").hide();
    };

    function showSuccessScreen (){
        jQuery("#loading-message").hide();
        jQuery("#success-message").show();
    };

    function addErrorMessage(message) {
        $scope.errorMsg.message.push(message);
    }


    var config = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE',
        'Access-Control-Max-Age': '3600',
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
        'Content-Type': 'application/text',
        'Access-Control-Allow-Credentials': false
    };

    $scope.init = function () {
        getAllMission();
    };

    function getAllMission() {
        toggleLoadingScreen();
        $http.get(baseurl + RESTMISSION)
            .then(function(data) {
                $log.debug(data);
                showSuccessScreen();
            })
            .catch(function(data) {
                $log.debug("Failed to send GET request");
                $log.debug(data);
            });
    }
});