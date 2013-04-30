
var lat;
var lng;
var radius;
var zone = [];

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

function initialize() {
	var mapOptions = {
	  center: new google.maps.LatLng(38.770949, -9.196243),
	  zoom: 12,
	  mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	var map = new google.maps.Map(document.getElementById("map_canvas"),
	    mapOptions);

	var marker = new google.maps.Marker({
      position: mapOptions.center,
      map: map,
      title:"Hello World!"
  	});

	var drawingManager = new google.maps.drawing.DrawingManager({
	  drawingMode: google.maps.drawing.OverlayType.MARKER,
	  drawingControl: true,
	  drawingControlOptions: {
	    position: google.maps.ControlPosition.TOP_CENTER,
	    drawingModes: [
	      google.maps.drawing.OverlayType.CIRCLE
	    ]
	  },
	  circleOptions: {
	    fillColor: '#00FF00',
	    fillOpacity: 0.2,
	    strokeWeight: 5,
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
        console.log(zone);
    });

	drawingManager.setMap(map);
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