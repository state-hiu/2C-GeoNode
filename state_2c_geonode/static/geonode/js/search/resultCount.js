(function(){
var module = angular.module('geonode_main_search');

module.directive('resultCount', function(){
  return {
    template: "<span style='font-size:34px;'>{{counts}} datasets found<span ng-hide='hideQuery()'> for &quot;{{query}}&quot;</span>",
    scope: {
      counts: '=',
      query: '='
    },
    link: function(scope, elem) {
      scope.hideQuery = function() {
        return((!scope.query || scope.query === "") ? true : false);
      };
    }
  };
});
})();
