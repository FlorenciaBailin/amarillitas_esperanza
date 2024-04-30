var latitud = document.getElementById('latitud').value;
var longitud = document.getElementById('longitud').value;

mapboxgl.accessToken = 'pk.eyJ1IjoiYXJpZWxjdmN4IiwiYSI6ImNsdmJuNXBvYjBhbHkya3FtZ2d1dG50cTIifQ.0m8_eMRY8yqswpGtGwy8iw';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [longitud, latitud],
    zoom: 13
});

new mapboxgl.Marker()
    .setLngLat([longitud, latitud])
    .addTo(map);

var geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    mapboxgl: mapboxgl,
    container: 'geocoder-container',
    zoom: 14,
    flyTo: { 
        speed: 1 
    }
});
geocoder.setProximity({ longitude: longitud, latitude: latitud });

map.addControl(geocoder);

geocoder.on('result', function (ev) {
    // Actualizar el valor del campo oculto con la información de la ubicación
    document.getElementById('adress').value = JSON.stringify(ev.result);
});