/**
 * Created by Joseph Tran on 1/10/2016.
 * This is a helpful REST API
 * https://thinkster.io/django-angularjs-tutorial
 */

var webserver = angular.module("webserver", []);
webserver.service("missionService", ["$scope", "$log", function ($scope, $log) {
    $log.debug("test");
}]);
webserver.controller("missionController", ["missionService", function($scope, $log, data)
{

}]);
