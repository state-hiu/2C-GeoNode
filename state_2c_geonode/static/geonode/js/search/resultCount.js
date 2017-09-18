(function(){
var module = angular.module('geonode_main_search');

module.directive('resultCount', ['$rootScope', function($rootScope){
  return {
    template: "<span style='font-size:34px;'>"    +
	      "    <span ng-show='showLoading'>" +
	      "        <img style='width: 30px;margin-right: 6px;margin-bottom: 6px;'" +
	      "        src='{{svgurl}}img/spinner.svg' alt='...'>Loading...</span>"    +
	      "    <span ng-hide='showLoading'>{{counts_}} datasets found" +
	      "        <span ng-hide='hideQuery()'> for <i>{{query_}}</i>  </span>"    +
	      "    </span>" +
	      "</span>",
    scope: {
      counts: '=',
      query: '=',
      svgurl: '@'
    },
    link: function(scope, elem) {
      scope.showLoading = true;
      scope.query_ = scope.query;

      scope.hideQuery = function() {
        return((!scope.query_ || scope.query_ === "") ? true : false);
      };

      scope.$on('performingSearch', function(e){
      	scope.showLoading = true;
      });

      scope.$on('searchPerformed', function(e, data){
	scope.query_ = data.meta.title__icontains;
	scope.counts_ = data.meta.total_count;
	scope.showLoading = false;
      });
    }
  };

}]);
})();
