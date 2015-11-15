'use strict';

var app = angular.module('nuslearn', ['angularFlaskServices', 'ngStorage', 'ngRoute', 'oblador.lazytube']);

app.directive('nonSuckyYoutubeEmbed', function factory() {
	var directiveDefinitionObject = {
		restrict: 'E',
		template: 	'<div style="position: relative;">' +
				  		'<img src="img/play-btn.png" style="position: absolute; left: 50%; top: 50%; width: 48px; height: 48px; margin-left: -24px; margin-top: -24px; cursor: pointer;" alt="Play" />' +
				  		'<img src="http://i.ytimg.com/vi/{{id}}/0.jpg" style="width: 100%; height: auto; display: inline; cursor: pointer" alt="" />' +
				  	'</div>',
		scope: {
			id: '@id'
		},
		link: function(scope, element, attrs) {
			attrs.$observe('id', function(id) {
				if(id) {
					var height = (attrs.height) ? attrs.height : 390;
					var width = (attrs.width) ? attrs.width : 640;
					var paddingBottom = ((height / width) * 100) + '%';
					var iframeStyle = 'position: absolute; top: 0; left: 0; width: 100%; height: 100%';
					var iframeContainerStyle = 'position: relative; padding-bottom: '+paddingBottom+'; padding-top: 30px; height: 0; overflow: hidden;'
					element.on('click', function() {
						var v = '<iframe type="text/html" style="'+iframeStyle+'" width="'+width+'" height="'+height+'" src="http://youtube.com/embed/'+id+'?autoplay=1" frameborder="0" />'
						var newHTML =	'<div style="'+iframeContainerStyle+'">' + v + '</div>';
						element.html(newHTML);
					});
				}
			});
		}
	};
	return directiveDefinitionObject;
});

// app.directive('ngEnter', function () {
//     return function (scope, element, attrs) {
//         element.bind("keydown keypress", function (event) {
//             if(event.which === 13) {
//                 scope.$apply(function (){
//                     scope.$eval(attrs.ngEnter);
//                 });
//
//                 event.preventDefault();
//             }
//         });
//     };
// });

app.run(function($rootScope, $window, $localStorage, $sce){
	if($localStorage.token){
		$rootScope.buttonTitle = "Logout";
	}else{
		$rootScope.buttonTitle = "Login";
	}

	$rootScope.login = function() {
		alert("Loggin");

		var apiKey = "yWIyIVdgoDbQz9EUdJ06x";
		var lapiURL = "https://ivle.nus.edu.sg/api/login/?apikey=";
		var appURL = "http://0.0.0.0:5000/loginProxy";
		var loginURL = lapiURL + apiKey + "&url=" + appURL;

		$window.location.replace(loginURL);
	};

}).filter('trustUrl', function ($sce) {
    return function(url) {
      return $sce.trustAsResourceUrl(url);
    };
  });

app.config(['$routeProvider', '$locationProvider',
function($routeProvider, $locationProvider, $window, $localStorage) {

	$locationProvider.html5Mode({
		enabled: true,
		requireBase: false
	});
	// $locationProvider.html5Mode(true);

	var checkRoute = function($localStorage, $location) {
		if ($localStorage.token) {
			$location.path('/loggedIn');
			return true;
		}else{
			$location.path('/');
			return false;
		}
	};

	$routeProvider
	.when('/', {
		templateUrl: 'static/partials/landing.html',
		controller: IndexController,
		resolve: {
			factory : checkRoute
		}
	}).when('/loginProxy', {
		templateUrl: 'static/partials/landing.html',
		controller: LoginProxyController,
	})
	// http://0.0.0.0:5000/loggedIn?token=6D3E16BCF94F492ACEAC385617895CD7C6D60E557E66D17C3E984F406AF3D59001B3A50D9589B6962D044AB903A15F21491961218C7C211BCE7281B776310AF301AF49D4D403F1ADE85D46DF800FC9B39D604244146412C6AA1F05E51524E2060F95C029E37AB731C54854AC704180021A8189F807F2B60D480D5B9C06D2C934186D20ED172201772D931D12EC776D25B5788D6325070E61D2EDF07DC369FE14C84BCBCDB1D7E40090CA1C9EAE6E6E5D8F5A079A8998DE7AAC4171E9AE0E2AD2E7F79BAE8F6AD3ACFF962FB98449114706A689AA4110A02DD7043133D52C9A9258A3BB07E1C0743EB7A546362F3AF9B0
	.when('/loggedIn', {
		templateUrl: 'static/partials/loggedIn.html',
		controller: LoginController,
		resolve: {
			factory : checkRoute
		}
	})
	.otherwise({
		redirectTo: '/'
	});

}])
;
