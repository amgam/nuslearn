'use strict';

angular.module('AngularFlask', ['angularFlaskServices'])
	.config(['$routeProvider', '$locationProvider',
		function($routeProvider, $locationProvider, $window) {
		$routeProvider
		.when('/', {
			templateUrl: 'static/partials/landing.html',
			controller: IndexController
		})

		// http://0.0.0.0:5000/loggedIn?token=6D3E16BCF94F492ACEAC385617895CD7C6D60E557E66D17C3E984F406AF3D59001B3A50D9589B6962D044AB903A15F21491961218C7C211BCE7281B776310AF301AF49D4D403F1ADE85D46DF800FC9B39D604244146412C6AA1F05E51524E2060F95C029E37AB731C54854AC704180021A8189F807F2B60D480D5B9C06D2C934186D20ED172201772D931D12EC776D25B5788D6325070E61D2EDF07DC369FE14C84BCBCDB1D7E40090CA1C9EAE6E6E5D8F5A079A8998DE7AAC4171E9AE0E2AD2E7F79BAE8F6AD3ACFF962FB98449114706A689AA4110A02DD7043133D52C9A9258A3BB07E1C0743EB7A546362F3AF9B0
		.when('/loggedIn', {
			templateUrl: 'static/partials/loggedIn.html',
			controller: LoginController
		})
		.when('/post', {
			templateUrl: 'static/partials/post-list.html',
			controller: PostListController
		})
		.when('/post/:postId', {
			templateUrl: '/static/partials/post-detail.html',
			controller: PostDetailController
		})
		/* Create a "/blog" route that takes the user to the same place as "/post" */
		.when('/blog', {
			templateUrl: 'static/partials/post-list.html',
			controller: PostListController
		})
		.otherwise({
			redirectTo: '/'
		})
		;

		$locationProvider.html5Mode(true);
	}])
;
