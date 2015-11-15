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
	$rootScope.logged = true;

	$scope.limit = 8;
	// console.log($localStorage.token);
	// console.log("success");
	//get username
	$http.get("/getusername")
	.success(function(response) {
		$rootScope.username = response.replace(/['"]+/g, '').toLowerCase();
	});

	//get user modules
	$http.get("/getmodulevideos")
	.success(function(response) {
		// console.log(response["CS2108"]);
		console.log(response);
		// $scope.userModInfo = response;
		$scope.moduleLinks = response;
	});

	if($localStorage.token){
		// $rootScope.buttonTitle = "Logout";
		$rootScope.login = function(){
			delete $localStorage.token;
			$rootScope.username = "";
			$rootScope.logged = false;
			$rootScope.buttonTitle = "Login";
			$location.path('/');
		};
	}else{
		$rootScope.buttonTitle = "Login";
		$rootScope.logged = true;
	}

	$scope.isSearch = true;

	$scope.chooseThis = function() {
		$scope.isSearch = !$scope.isSearch;
	};

	$scope.submit = {};
	$scope.submit["tags"] = "";

	$scope.suggest = function() {

		$http({
			method: 'POST',
			url: "/suggest",
			data: $scope.submit,
			headers: {'Content-Type': 'application/x-www-form-urlencoded'}
		}).success(function(response){
			// $scope.suggestionResponse = response;

			$scope.good = false;
			$scope.modprob = false;
			$scope.linkprob = false;

			var msg = response["err"];

			if(msg == "good"){
				$scope.good = true;
			}else if(msg == "modprob"){
				$scope.modprob = true;
			}else{
				// link prob
				$scope.linkprob = true;
			}

			console.log(response);
		});
	};




	$scope.searchTerm = {};
	$scope.searchTerm["term"] = "";

	$scope.clear = function() {
		$scope.searchTerm["term"] = "";
		$scope.moduleLinks = $scope.search();
	};

	$scope.search = function(){
		$http({
			method: 'POST',
			url: "/search",
			data: $scope.searchTerm,
			headers: {'Content-Type': 'application/x-www-form-urlencoded'}
		}).success(function(response){
			console.log("search done.");
			console.log(response);

			if($scope.searchTerm["term"] == ""){
				$http.get("/getmodulevideos")
				.success(function(response) {
					// console.log(response["CS2108"]);
					console.log(response);
					// $scope.userModInfo = response;
					$scope.moduleLinks = response;
				});

			}else{
				$scope.moduleLinks = response;
			}
		});
	};


	// $scope.thumbs = {};
	// $scope.thumbs["upvote"] = "";
	$scope.thumbedup = function(index){
		
	};


	$scope.thumbsup = function(vid_link, searchT){
				$http({
					method: 'POST',
					url: "/upvote",
					data: {"upvote": vid_link, "searchT": searchT},
					headers: {'Content-Type': 'application/x-www-form-urlencoded'}
				}).success(function(response){
					$scope.moduleLinks = response;
					// $scope.userModInfo = response;
					console.log(response);
				});
	};

	$scope.thumbsdown = function(vid_link, searchT){
		$http({
			method: 'POST',
			url: "/downvote",
			data: {"downvote": vid_link, "searchT": searchT},
			headers: {'Content-Type': 'application/x-www-form-urlencoded'}
		}).success(function(response){
			$scope.moduleLinks = response;
			// $scope.userModInfo = response;
			console.log(response);
		});
	};

}
