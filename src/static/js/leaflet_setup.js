
function Get(yourUrl){
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("GET",yourUrl,false);
    Httpreq.send(null);
    return JSON.parse(Httpreq.responseText);
}

function onMapClick(e) {
    var lat = e.latlng.lat;
    var lon = e.latlng.lng;
    var url = "/click?lat=" + lat + "&lon="+lon;
    var latlngs = Get(url);
    drawSegment(latlngs);
}

function drawSegment(latlngs) {
    var last = latlngs[latlngs.length-1];
    var center = latlngs[Math.floor(latlngs.length/2)];
    L.polyline(latlngs).addTo(map);
    L.marker([last[0], last[1]]).addTo(map);
    L.marker([center[0], center[1]]).addTo(map).setIcon(L.divIcon({
	className: 'marker',
        html: "<div>Hello</div>"
    }));
}

var map;

window.onload = (e) => {
    map = L.map('map').setView([51.505, -0.09], 13);

    map.on('click', onMapClick);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    latlngs = Get("/poly")
    latlngs.forEach((value) => {
        drawSegment(value);
    })

    // Add the first marker
    var lastLatLng = latlngs[0];
    var lastPoint = lastLatLng[0]
    L.marker([lastPoint[0], lastPoint[1]]).addTo(map).setIcon(L.divIcon({
	className: 'marker',
        html: "<div>Hello</div>"
    }));


}
