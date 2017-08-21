(function(){
var module = angular.module('geonode_main_search');

module.directive('resultCount', function(){
  return {
    template: "<span style='font-size:34px;'>{{counts}} datasets found<span ng-hide='query == \"\"'> for &quot;{{query}}&quot;</span>",
    scope: {
      counts: '=',
      query: '='
    }
  };
});
})();
