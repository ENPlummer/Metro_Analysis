
// Create the function to determine the marker color based on the number or riders.
function getColor(d) {
	return  d > 30000 ? '#023858':
			d > 25000 ? '#045a8d':
			d > 20000 ? '#0570b0':
			d > 15000 ? '#3690c0':
			d > 10000 ? '#74a9cf':
			d > 5000 ?  '#a6bddb':
			d > 2000 ?  '#d0d1e6':
			d > 1000 ?  '#ece7f2':
						'#fff7fb';
						
}

// Store the API endpoint inside the queryURL.

//var queryURL = "https://rawgit.com/ENPlummer/c7fde15929501bc27b412aa053045d53/raw/ae728e1cd40d2a7692a0bf7568ec384aff6a4f06/metro.geojson"

var queryURL = "https://gist.github.com/ENPlummer/c7fde15929501bc27b412aa053045d53"
// Perform a GET request to query the URL.
d3.json(queryURL,function(data) {
	//CreateFeatures object for the Create features function.
	createFeatures(data.features);
});

function createFeatures(metroData) {
	function onEachFeature(feature, layer) {
		layer.bindPopup("<h2>" + feature.properties.STATION + "<h3><hr><p>" +
		 feature.properties.RIDERS_PER_WEEKDAY + " Riders per Weekday<p>");
	}

	var metroStations = L.geoJSON(metroData, {
		onEachFeature: onEachFeature,
		pointToLayer: pointToLayer
	});

	//Sending the metroStations layer to the createMap function.
	createMap(metroStations);

	function pointToLayer(feature, latlag) {
		return L.circle(latlag, {
			stroke: false,
			fillOpacity: 0.7,
			fillColor: getColor(feature.properties.RIDERS_PER_WEEKDAY),
			radius: feature.properties.RIDERS_PER_WEEKDAY/15
		})
	}
}



function createMap(metro) {
	//Define outdoor and satellite map layers.
	var outdoorMap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/outdoors-v10/tiles/256/{z}/{x}/{y}?" +
		"access_token=pk.eyJ1IjoibXVzaWNhbGVib255IiwiYSI6ImNqaDl3eTdteTAzcmgzMG82bnF2YzBqbG4ifQ.lEEqXiYOx4ZFGzwfC6elgQ");
    var streetMap = L.tileLayer("http://api.mapbox.com/v4/mapbox.streets-basic.html?" + 
    	"access_token=pk.eyJ1IjoibXVzaWNhbGVib255IiwiYSI6ImNqaDl3eTdteTAzcmgzMG82bnF2YzBqbG4ifQ.lEEqXiYOx4ZFGzwfC6elgQ");
    var baseMaps = {
    	"Outdoor Map":outdoorMap,
    	"Street Map":streetMap
    };

    //Create an overlay object to hold the overlay layer.
    var overlayMaps = {
    	Metro: metro
    };

    //Create the map giving it the outdoormak and earthquake layers to display the map on load.
    var myMap = L.map("map",{
    	center: [38.91, -77.04],
    	zoom: 12,
    	layers:[outdoorMap, streetMap, metro]
    });

    //Create a layer control.
    //Pass in the baseMaps and overlayMaps
    //Add the control layer to the map.
    L.control.layers(baseMaps,overlayMaps,{
    	collapse: false
    }).addTo(myMap);
    //Add a legend to the map.

    var legend = L.control({position: "bottomright"});

  legend.onAdd = function(myMap) {

    	var div = L.DomUtil.create("div", "info legend"),
    	grades = [500, 1000, 2000, 5000, 10000, 15000, 20000, 25000]
    	labels = [];

    	for (var i = 0; i < grades.length; i++) {
    		div.innerHTML +=
    		'<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+')
    	}

    	return div
   };

   legend.addTo(myMap);
	};