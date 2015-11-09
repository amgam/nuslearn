'use strict';

/* Controllers */

function IndexController($scope, $window, $location) {
	alert('index');
	$scope.title = "nuslearn";

	$scope.login = function() {
		alert("Loggin");

	var apiKey = "yWIyIVdgoDbQz9EUdJ06x";
	var lapiURL = "https://ivle.nus.edu.sg/api/login/?apikey=";
	var appURL = "http://0.0.0.0:5000/loginProxy";
	var loginURL = lapiURL + apiKey + "&url=" + appURL;
	//
	$window.location.replace(loginURL);
	};
}

function LoginProxyController($scope, $routeParams, $location, $localStorage) {
	alert('logged in!');
	// var t = $routeParams.accessToken;
	$localStorage.token = $location.search().token
	$location.path('/loggedIn');

	// console.log("DONE");
}

function LoginController($scope, $localStorage, $location){
	console.log($localStorage.token);
	console.log("success");

	$scope.logout = function(){
		delete $localStorage.token;
		$location.path('/');
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
