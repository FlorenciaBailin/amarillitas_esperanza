/* Ariel Avila - 29-04-2024 MB01: Se Agrega el token */
mapboxgl.accessToken = 'pk.eyJ1IjoiYXJpZWxjdmN4IiwiYSI6ImNsdmJuNXBvYjBhbHkya3FtZ2d1dG50cTIifQ.0m8_eMRY8yqswpGtGwy8iw';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [-70.738129,-33.710423], // Aca podemos cambiar la longitud y latitud para que aparezca centrado el mapa donde queramos
    zoom: 9
});

var geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    mapboxgl: mapboxgl,
    container: 'geocoder-container'
});

map.addControl(geocoder);

geocoder.on('result', function (ev) {
    map.flyTo({
        center: ev.result.geometry.coordinates,
        zoom: 14
    });
    // Actualizar el valor del campo oculto con la información de la ubicación
    document.getElementById('adress').value = JSON.stringify(ev.result);
});
