
var lat;
var lng;
var radius;
var zone = [];
window.myzone=[];

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
	// test that a given url is a same-origin URL
	// url could be relative or scheme relative or absolute
	var host = document.location.host; // host + port
	var protocol = document.location.protocol;
	var sr_origin = '//' + host;
	var origin = protocol + sr_origin;
	// Allow absolute or scheme relative URLs to same origin
	return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
		(url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
		// or any other URL that isn't scheme relative or absolute i.e relative.
		!(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
			// Send the token to same-origin, relative URLs only.
			// Send the token only if the method warrants CSRF protection
			// Using the CSRFToken value acquired earlier
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
});

function getUrlVars() {
	var vars = {};
	var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
		vars[key] = value;
	});
	return vars;
}

/*****************************************************************************************************
									 MAP RELATED FUNCTIONS
******************************************************************************************************/
function initialize() {
	var mapOptions = {
	  center: new google.maps.LatLng(38.770949, -9.196243),
	  zoom: 4,
	  mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	var map = new google.maps.Map(document.getElementById("map_canvas"),mapOptions);

	// Try HTML5 geolocation
	if(navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(function(position) {
			var pos = new google.maps.LatLng(position.coords.latitude,
				position.coords.longitude);

			var infowindow = new google.maps.InfoWindow({
				map: map,
				position: pos,
				content: 'Location found using HTML5.'
			});
			console.log(pos.lat());
			console.log(pos.lng());
			map.setCenter(pos);
		}, function() {
			handleNoGeolocation(true);
		});
	} else {
	    // Browser doesn't support Geolocation
	    handleNoGeolocation(false);
	}

	// Using Drawing Manager Library to draw on the map
	var drawingManager = new google.maps.drawing.DrawingManager({
	  drawingMode: google.maps.drawing.OverlayType.CIRCLE,
	  drawingControl: true,
	  drawingControlOptions: {
	    position: google.maps.ControlPosition.TOP_CENTER,
	    drawingModes: [
	      google.maps.drawing.OverlayType.CIRCLE
	    ]
	  },
	  circleOptions: {
	    fillColor: '#00FF00',
	    fillOpacity: 0.4,
	    clickable: true,
	    zIndex: 1,
	    editable: true
	  }
	});

	var coord_listener = google.maps.event.addListener(drawingManager, 'circlecomplete', function (circle) {
        lat = circle.getCenter().lat();
        lng = circle.getCenter().lng();
        radius = circle.getRadius();

        zone.push({
        	"lat" : lat,
        	"lng" : lng,
        	"radius" : radius
        });
    });

	if (typeof window.myzone[0] != 'undefined') {
		draw_circle = new google.maps.Circle({
	        center: new google.maps.LatLng(window.myzone[0]["lat"], window.myzone[0]["lng"]),
	        radius: window.myzone[0]["radius"] * 1000.0,
	        fillColor: '#00FF00',
	        fillOpacity: 0.4,
	        map: map
	 	});
	}	
	drawingManager.setMap(map);
}

function handleNoGeolocation(errorFlag) {
	if (errorFlag) {
	var content = 'Error: The Geolocation service failed.';
	} else {
	var content = 'Error: Your browser doesn\'t support geolocation.';
	}

	var options = {
	map: map,
	position: new google.maps.LatLng(60, 105),
	content: content
	};

	var infowindow = new google.maps.InfoWindow(options);
	map.setCenter(options.position);
}

function addfriend(){
	var friendname=window.location.pathname.split("/");
	$.post("meeting/add_friend",{friendname : JSON.stringify(friendname[1])},function(data,status){
            console.log(status);
            alert("Friend added!!");
    });
}

function savezone(){
	$.post("meeting/save_zone",{zones : JSON.stringify(zone)},function(data,status){
            alert("YOUR ZONES ARE SAVED");
    });
}