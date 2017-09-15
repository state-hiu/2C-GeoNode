(function(){
var module = angular.module('geonode_main_search');

module.directive('resultCount', ['$rootScope', function($rootScope){
  return {
    template: "<span style='font-size:34px;'>"    +
	      "    {{counts_}} datasets found"     +
	      "    <span ng-hide='hideQuery()'> for <i>{{query_}}</i>  </span>" +
	      "</span>",
    scope: {
      counts: '=',
      query: '='
    },
    link: function(scope, elem) {
      scope.query_ = scope.query;

      scope.hideQuery = function() {
        return((!scope.query_ || scope.query_ === "") ? true : false);
      };

      scope.$on('searchPerformed', function(e, data){
	scope.query_ = data.meta.title__icontains;
	scope.counts_ = data.meta.total_count;
      });
    }
  };

}]);
})();
