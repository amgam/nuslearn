'use strict';

/* Controllers */

function IndexController($scope, $window, $location, $rootScope) {
	// alert('index');
	$scope.title = "nuslearn";

	$rootScope.login = function() {
		// alert("Loggin");

		var apiKey = "yWIyIVdgoDbQz9EUdJ06x";
		var lapiURL = "https://ivle.nus.edu.sg/api/login/?apikey=";
		var appURL = "http://0.0.0.0:5000/loginProxy";
		var loginURL = lapiURL + apiKey + "&url=" + appURL;
		//
		$window.location.replace(loginURL);
	};
}

function LoginProxyController($rootScope, $routeParams, $location, $localStorage) {
	// alert('logged in!');
	// var t = $routeParams.accessToken;
	$localStorage.token = $location.search().token
	$rootScope.buttonTitle = "Logout";
	$location.path('/loggedIn');

	// console.log("DONE");
}

function LoginController($rootScope, $localStorage, $location, $http, $scope, $sce){
	// console.log($localStorage.token);
	// console.log("success");

	//get username
	$http.get("/getusername")
	.success(function(response) {
		$rootScope.username = response.replace(/['"]+/g, '').toLowerCase();
	});

	//example!
	$scope.raw_links = [
		{"title": "hysteria", "module": "music", "desc": "bassss", "link": "https://www.youtube.com/embed/0FECUG7k5gY", "votes" : 15},
		{"title": "bass less", "module": "music", "desc": "slap bass", "link": "https://www.youtube.com/embed/4PKqsRseid8", "votes": 32},
		{"title": "505", "module": "music", "desc": "505 live", "link": "https://www.youtube.com/embed/aZv8tmvCGPE", "votes" : 100}
	];

	//get user modules
	$http.get("/getmodules")
	.success(function(response) {
		// console.log(response["CS2108"]);
		$scope.modules = response;
		// $rootScope.username = response.replace(/['"]+/g, '').toLowerCase();
	});

	if($localStorage.token){
		// $rootScope.buttonTitle = "Logout";
		$rootScope.login = function(){
			delete $localStorage.token;
			$rootScope.username = "";
			$rootScope.buttonTitle = "Login";
			$location.path('/');
		};
	}else{
		$rootScope.buttonTitle = "Login";
	}

	$scope.isSearch = true;

	$scope.chooseThis = function() {
		$scope.isSearch = !$scope.isSearch;
	};

}
