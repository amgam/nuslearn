'use strict';

/* Controllers */

function IndexController($scope, $window, $location) {
	alert('index');
	$scope.title = "nuslearn";

	$scope.login = function() {
		// alert("Loggin");

	// var apiKey = "yWIyIVdgoDbQz9EUdJ06x";
	// var lapiURL = "https://ivle.nus.edu.sg/api/login/?apikey=";
	// var appURL = "http://0.0.0.0:5000/loggedIn";
	// var loginURL = lapiURL + apiKey + "&url=" + appURL;
	//
	// $window.location.href = loginURL;
	alert("trying to login");
	$location.path('/loggedIn');
	};
}

function LoginController($scope, $routeParams) {
	alert('login');
	console.log($routeParams.token);
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
