
	
	
	



	//This function accepts JSON in the form of the following
	// {lat:30.0923,log:-77.037,weight:98}
	//It populates 2 sets of google maps data, one weighted and one regular
	// the regular just sets all weights to 1.
	function PushGeoData(geoData)
	{
		alert(geoData[1].lat);
		for(var i = 0; i < geoData.length; i++) 
		{
			
			var latLng = new google.maps.LatLng(geoData[i].lat, geoData[i].log);
			var weightedLoc = 
			{
				location: latLng,
				weight: geoData[i].weight
			};
			var regularLoc =
			{
				location: latLng,
				weight: 1
			};
			
			WeightedMapData.push(weightedLoc);
			RegularMapData.push(regularLoc);

		}
	}



		  function initialize()
		{
	  
			var mapOptions = {
			  center: new google.maps.LatLng(39.833333, -98.583333),
			  zoom: 4,
			  mapTypeId: google.maps.MapTypeId.SATELLITE
			}

		var mapCanvas = document.getElementById('map_canvas');

			map = new google.maps.Map(mapCanvas, mapOptions)
		  
		heatmap = new google.maps.visualization.HeatmapLayer({
		data: HeatMapData,
			radius:15

		});
		heatmap.setMap(map);

		}

	google.maps.event.addDomListener(window, 'load', initialize);






	function ChooseWeighted()
	{
		HeatMapData = WeightedMapData;
		initialize();
		PushGeoData(JsonGeoData);
	}

	function ChooseRegular()
	{
		HeatMapData = RegularMapData;
		initialize();
		PushGeoData(JsonGeoData);
	}


