/**
 * Created by Joseph Tran on 1/10/2016.
 * This is a helpful REST API
 * https://thinkster.io/django-angularjs-tutorial
 *
 * AngularJS tutorial
 * https://www.toptal.com/angular-js/a-step-by-step-guide-to-your-first-angularjs-app
 */

var webServer = angular.module("webServer", [])
.controller("missionCtrl", function($log, $scope)
{
    $log.debug("Hello world");

    $scope.currentMission = {};

    $scope.sayHiForMe = function () {
        $log.debug("YOU CLICKED ME!");
    };
});