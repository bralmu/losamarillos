"use strict";
var names;
var lat = [];
var lng = [];
var respuesta;
$.getJSON( "names", function( ndata ) {
	  names = ndata['names'];
	  $("body").append("<ul>");
	  for (var n in names) {
		  $.getJSON( "https://maps.googleapis.com/maps/api/geocode/json",
					{address: names[n]+", spain", key: APIKEY}, 
					(function(cn){
						return function(gldata) {
							respuesta = gldata;
							if(!gldata["results"][0]) {
								console.log("No geolocation for "+names[cn]);
							}
							lat[cn] = gldata["results"][0]["geometry"]["location"]["lat"];
							lng[cn] = gldata["results"][0]["geometry"]["location"]["lng"];
							$("body").append("<li>"+names[cn]+" "+lat[cn]+" "+lng[cn]+"</li>");
						};
					}(n))
		  );		  
	  }
	  $("body").append("</ul>");
	});

/**
function(gldata) {
respuesta = gldata;
lat[cn] = gldata["results"][0]["geometry"]["location"]["lat"];
lng[cn] = gldata["results"][0]["geometry"]["location"]["lng"];
$("body").append("<li>"+names[cn]+" "+lat[cn]+" "+lng[cn]+"</li>");
}
**/