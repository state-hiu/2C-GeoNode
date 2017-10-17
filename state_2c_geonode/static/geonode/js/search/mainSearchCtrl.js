'use strict';

(function(){
  /*
  * Main search controller
  * Load data from api and defines the multiple and single choice handlers
  * Syncs the browser url with the selections
  */
  var module = angular.module('geonode_main_search');
 
  module.controller('main_geonode_search_controller', function($rootScope, $injector, $scope, $location, $http, Configs){
    $scope.query = $location.search();
    $scope.query.limit = $scope.query.limit || CLIENT_RESULTS_LIMIT;
    $scope.query.offset = $scope.query.offset || 0;
    $scope.page = Math.round(($scope.query.offset / $scope.query.limit) + 1);
   

    //Get data from apis and make them available to the page
    function query_api(params){
	$rootScope.$broadcast('performingSearch');
	$http.get(Configs.url, {params: params || {}}).success(function(data){
	data.meta.title__icontains = params.q;
	    $scope.countKeywords = countByKeywords(data.objects);
            $scope.results = joinLayersBy_uuid(data.objects);
     	    $scope.total_counts = data.meta.total_count;
            $scope.$root.query_data = data;
	    $rootScope.$broadcast('searchPerformed', data);
	    
	    if (HAYSTACK_SEARCH) {
                if ($location.search().hasOwnProperty('q')){
                   $scope.text_query = $location.search()['q'].replace(/\+/g," ");
                }
            } else {
                if ($location.search().hasOwnProperty('title__icontains')){
                    $scope.text_query = $location.search()['title__icontains'].replace(/\+/g," ");
                }
            }

            //Update facet/keyword/category counts from search results
            if (HAYSTACK_FACET_COUNTS){
                module.haystack_facets($http, $scope.$root, $location);
                $("#types").find("a").each(function(){
                    if ($(this)[0].id in data.meta.facets.subtype) {
                        $(this).find("span").text(data.meta.facets.subtype[$(this)[0].id]);
                    } 
                    else if ($(this)[0].id in data.meta.facets.type) {
                        $(this).find("span").text(data.meta.facets.type[$(this)[0].id]);
                    } else {
                        $(this).find("span").text("0");
                    }
                });
            }
        });
    };
    query_api($scope.query);

    function joinLayersBy_uuid(objects){
        // Prepare the first object
	if(objects.length === 0){
	    return [];
	}

        var prepareObject = objects[0];
        var keywords = [prepareObject.keywords__name];

        var mergedArray = [];
        
        for (var i = 1; i < objects.length; i++) {
            var currObj = objects[i];

            if (currObj.uuid === prepareObject.uuid) {
                keywords.push(currObj.keywords__name);
            }else {
                prepareObject.keywords__name = keywords;
                mergedArray.push(prepareObject);

                prepareObject = currObj
                keywords = [currObj.keywords__name];
            }
        }

        // push the las item
        prepareObject.keywords__slug = keywords;
        mergedArray.push(prepareObject);

        return mergedArray;
    }

    function countByKeywords(objects) {
        var keywordsCount = {}; 
        objects.map(function(obj) {
            return obj.keywords__name;
        })
        .sort()
        .map(function(kw){
            if (keywordsCount[kw]) {
                keywordsCount[kw]++;
            }else{
                keywordsCount[kw] = 1;
            }
        });
        return keywordsCount;
    }

	
    $scope.setActiveCategories = function(value){	
	if('category__identifier__in' in $scope.query){
	    var category = $scope.query['category__identifier__in'];
	    if(category === value) return 'active';

	    for(var item of category){
		if(value === item){
		    return 'active';
	        }
	    }
	}
    };
 
   /*
    * Pagination
    */
    // Control what happens when the total results change
    $scope.$watch('total_counts', function(){
      $scope.numpages = Math.round(
        ($scope.total_counts / $scope.query.limit) + 0.49
      );

      // In case the user is viewing a page > 1 and a
      // subsequent query returns less pages, then
      // reset the page to one and search again.
      if($scope.numpages < $scope.page){
        $scope.page = 1;
        $scope.query.offset = 0;
        query_api($scope.query);
      }

      // In case of no results, the number of pages is one.
      if($scope.numpages == 0){$scope.numpages = 1};
    });

    $scope.paginate_down = function(){
      if($scope.page > 1){
        $scope.page -= 1;
        $scope.query.offset =  $scope.query.limit * ($scope.page - 1);
        query_api($scope.query);
      }
    }

    $scope.paginate_up = function(){
      if($scope.numpages > $scope.page){
        $scope.page += 1;
        $scope.query.offset = $scope.query.limit * ($scope.page - 1);
        query_api($scope.query);
      }
    }
    /*
    * End pagination
    */


    if (!Configs.hasOwnProperty("disableQuerySync")) {
        // Keep in sync the page location with the query object
        $scope.$watch('query', function(){
		$location.search($scope.query);
        }, true);
    }

    // Hyerarchical keywords listeners
    $scope.$on('select_h_keyword', function($event, element){
      var data_filter = 'keywords__slug__in';
      var query_entry = [];
      var value = element.text;
      // If the query object has the record then grab it
      if ($scope.query.hasOwnProperty(data_filter)){

        // When in the location are passed two filters of the same
        // type then they are put in an array otherwise is a single string
        if ($scope.query[data_filter] instanceof Array){
          query_entry = $scope.query[data_filter];
        }else{
          query_entry.push($scope.query[data_filter]);
        }
      }
  
      // Add the entry in the correct query
      if (query_entry.indexOf(value) == -1){
        query_entry.push(value);
      }

      //save back the new query entry to the scope query
      $scope.query[data_filter] = query_entry;

     query_api($scope.query);
    });

    $scope.$on('unselect_h_keyword', function($event, element){
      var data_filter = 'keywords__slug__in';
      var query_entry = [];
      var value = element.text;
      // If the query object has the record then grab it
      if ($scope.query.hasOwnProperty(data_filter)){

        // When in the location are passed two filters of the same
        // type then they are put in an array otherwise is a single string
        if ($scope.query[data_filter] instanceof Array){
          query_entry = $scope.query[data_filter];
        }else{
          query_entry.push($scope.query[data_filter]);
        }
      }
  
      query_entry.splice(query_entry.indexOf(value), 1);

      //save back the new query entry to the scope query
      $scope.query[data_filter] = query_entry;

      //if the entry is empty then delete the property from the query
      if(query_entry.length == 0){
        delete($scope.query[data_filter]);
      }
      query_api($scope.query);
    });

    /*
    * Add the selection behavior to the element, it adds/removes the 'active' class
    * and pushes/removes the value of the element from the query object
    */
    $scope.multiple_choice_listener = function($event){
      var element = $($event.target);
      var query_entry = [];
      var data_filter = element.attr('data-filter');
      var value = element.attr('data-value');
      var filterParams = $scope.query[data_filter];

      if($scope.query[data_filter] !== value){
          // If the query object has the record then grab it
	  if(data_filter in $scope.query){
              // When in the location are passed two filters of the same
              // type then they are put in an array otherwise is a single string
              if (Array.isArray($scope.query[data_filter])){
                  query_entry = $scope.query[data_filter];
              }else{
	          query_entry.push($scope.query[data_filter]);
	      }
	  }

          if(element.hasClass('active')){
              // clear the active class from it
              element.removeClass('active');
              // Remove the entry from the correct query in scope
              query_entry.splice(query_entry.indexOf(value), 1);
          } else {
              // Add the entry in the correct query
              if (query_entry.indexOf(value) === -1){
                  query_entry.push(value);
              }
              element.addClass('active');
          }

          //save back the new query entry to the scope query
          $scope.query[data_filter] = query_entry;
      }

      //if the entry is empty then delete the property from the query
      if(query_entry.length === 0){
        delete($scope.query[data_filter]);
      }
      query_api($scope.query);
    }

    $scope.single_choice_listener = function($event){
      var element = $($event.target);
      var query_entry = [];
      var data_filter = element.attr('data-filter');
      var value = element.attr('data-value');
      // Type of data being displayed, use 'content' instead of 'all'
      $scope.dataValue = (value == 'all') ? 'content' : value;

      // If the query object has the record then grab it
      if ($scope.query.hasOwnProperty(data_filter)){
        query_entry = $scope.query[data_filter];
      }

      if(!element.hasClass('selected')){
        // Add the entry in the correct query
        query_entry = value;

        // clear the active class from it
        element.parents('ul').find('a').removeClass('selected');

        element.addClass('selected');

        //save back the new query entry to the scope query
        $scope.query[data_filter] = query_entry;

        query_api($scope.query);
      }
    }

    /*
    * Text search management
    */
    var text_autocomplete = $('#text_search_input').yourlabsAutocomplete({
          url: AUTOCOMPLETE_URL_RESOURCEBASE,
          choiceSelector: 'span',
          hideAfter: 200,
          minimumCharacters: 1,
          placeholder: gettext('Enter your text here ...'),
          autoHilightFirst: false
    });

    $('#text_search_input').keypress(function(e) {
      if(e.which == 13) {
        $('#text_search_btn').click();
        $('.yourlabs-autocomplete').hide();
      }
    });

    $('#text_search_input').bind('selectChoice', function(e, choice, text_autocomplete) {
          if(choice[0].children[0] == undefined) {
              $('#text_search_input').val($(choice[0]).text());
              $('#text_search_btn').click();
          }
    });

    $('#text_search_btn').click(function(){
	if (HAYSTACK_SEARCH){
            $scope.query['q'] = $('#text_search_input').val();
        } else {
            if (AUTOCOMPLETE_URL_RESOURCEBASE === "/autocomplete/ProfileAutocomplete/"){
                // a user profile has no title; if search was triggered from
                // the /people page, filter by username instead
                var query_key = 'username__icontains';
            }else {
                var query_key = $( "#text_search_input" ).data( "queryKey" );
            }
	    $scope.query[query_key] = $('#text_search_input').val();
	}
        query_api($scope.query);
    });

    /*
    * Region search management
    */
    var region_autocomplete = $('#region_search_input').yourlabsAutocomplete({
          url: AUTOCOMPLETE_URL_REGION,
          choiceSelector: 'span',
          hideAfter: 200,
          minimumCharacters: 1,
          appendAutocomplete: $('#region_search_input'),
          placeholder: gettext('Enter your region here ...')
    });
    $('#region_search_input').bind('selectChoice', function(e, choice, region_autocomplete) {
          if(choice[0].children[0] == undefined) {
              $('#region_search_input').val(choice[0].innerHTML);
              $('#region_search_btn').click();
          }
    });

    $('#region_search_btn').click(function(){
        $scope.query['regions__name__in'] = $('#region_search_input').val();
        query_api($scope.query);
    });

    $scope.feature_select = function($event){
      var element = $($event.target);
      var article = $(element.parents('article')[0]);
      if (article.hasClass('resource_selected')){
        element.html('Select');
        article.removeClass('resource_selected');
      }
      else{
        element.html('Deselect');
        article.addClass('resource_selected');
      }
    };

    /*
    * Date management
    */

    $scope.date_query = {
      'date__gte': '',
      'date__lte': ''
    };
    var init_date = true;
    $scope.$watch('date_query', function(){
      if($scope.date_query.date__gte != '' && $scope.date_query.date__lte != ''){
        $scope.query['date__range'] = $scope.date_query.date__gte + ',' + $scope.date_query.date__lte;
        delete $scope.query['date__gte'];
        delete $scope.query['date__lte'];
      }else if ($scope.date_query.date__gte != ''){
        $scope.query['date__gte'] = $scope.date_query.date__gte;
        delete $scope.query['date__range'];
        delete $scope.query['date__lte'];
      }else if ($scope.date_query.date__lte != ''){
        $scope.query['date__lte'] = $scope.date_query.date__lte;
        delete $scope.query['date__range'];
        delete $scope.query['date__gte'];
      }else{
        delete $scope.query['date__range'];
        delete $scope.query['date__gte'];
        delete $scope.query['date__lte'];
      }
      if (!init_date){
        query_api($scope.query);
      }else{
        init_date = false;
      }

    }, true);

    /*
    * Spatial search
    */
    if ($('.leaflet_map').length > 0) {
      angular.extend($scope, {
        layers: {
          baselayers: {
            stamen: {
              name: 'Toner Lite',
              type: 'xyz',
              url: 'http://{s}.tile.stamen.com/toner-lite/{z}/{x}/{y}.png',
              layerOptions: {
                subdomains: ['a', 'b', 'c'],
                attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>',
                continuousWorld: true
              }
            }
          }
        },
        map_center: {
          lat: 5.6,
          lng: 3.9,
          zoom: 0
        },
        defaults: {
          zoomControl: false
        }
      });

			
      var leafletData = $injector.get('leafletData'),
          map = leafletData.getMap('filter-map');

      map.then(function(map){
        map.on('moveend', function(){
          $scope.query['extent'] = map.getBounds().toBBoxString();
          query_api($scope.query);
        });
      });
    
      var showMap = false;
      $('#_extent_filter').click(function(evt) {
     	  showMap = !showMap
        if (showMap){
          leafletData.getMap().then(function(map) {
            map.invalidateSize();
          });
        } 
      });
    }
  });
})();
