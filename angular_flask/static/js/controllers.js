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

function LoginController($rootScope, $localStorage, $location, $http, $scope){
	// console.log($localStorage.token);
	// console.log("success");

	$http.get("/getusername")
	.success(function(response) {
		// alert(response);
		$rootScope.username = response.replace(/['"]+/g, '').toLowerCase();
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
		$scope.isActive = !$scope.isActive;
	};

}

function PostListController($scope, Post) {
	var postsQuery = Post.get({}, function(posts) {
		$scope.posts = posts.objects;
	});
}

function PostDetailController($scope, $routeParams, Post) {
	var postQuery = Post.get({ postId: $routeParams.postId }, function(post) {
		$scope.post = post;
	});
}
