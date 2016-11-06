/**
 * Created by Joseph Tran on 6/11/2016.
 */

angular.module("webServer")
.service('restService', function($http, $log) {
    var baseurl = "http://localhost:5001/rest/";

    var config = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE',
        'Access-Control-Max-Age': '3600',
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
        'Content-Type': 'application/text',
        'Access-Control-Allow-Credentials': false
    };

    $log.debug(window.location.host);

    this.post = function (url, data) {
        return $http.post(baseurl + url, data, config);
    };

    this.get = function (url) {
        return $http.get(baseurl + url);
    };

    this.put = function (url) {
        return $http.put(url, {data: ""}, config);
    }
});