
//déclaration des couches openlayers
var lyr_osm = new ol.layer.Tile({
    title: 'OSM',
    type: 'base',
    visible: true,
    source: new ol.source.OSM()
});


var markerStyle = new ol.style.Style({
    image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
      anchor: [1, 1],
      anchorXUnits: 'fraction',
      anchorYUnits: 'fraction',
      src: './static/icon.png',
      scale: 0.3
    }))
});

var sectors = new ol.source.Vector({
    format: new ol.format.GeoJSON(),
    url: './static/NYPD Sectors.geojson'
})
var sectorLayer = new ol.layer.Vector({
    source: sectors
});

var station =  new ol.source.Vector({
    format: new ol.format.GeoJSON(),
    url: './static/NYCHA PSA (Police Service Areas).geojson',
})

var stationVectors  = new ol.layer.Vector({
    source: station,
    style: markerStyle,
    
});

//visibilité par défaut des couches au chargement de la carte
lyr_osm.setVisible(true)

//déclaration de la liste des couches à afficher dans un ordre précis
var layersList = [ lyr_osm, sectorLayer, stationVectors ];

//Definition des popups pour affichage des infos
var container = document.getElementById('popup');
var content = document.getElementById('popup-content');
var closer = document.getElementById('popup-closer');
closer.onclick = function() {
    container.style.display = 'none';
    closer.blur();
    return false;
};


var overlayPopup = new ol.Overlay({
    element: container
});

var mapView = new ol.View({
    projection: 'EPSG:4326',
    center:[-73.920935, 40.780229],
    zoom: 10
});
var map = new ol.Map({
    target: 'map',
    overlays: [overlayPopup],
    layers: layersList,
    view: mapView
});

var layerSwitcher = new ol.control.LayerSwitcher({
    tipLabel: 'Légende'
});
map.addControl(layerSwitcher);

var MousePosition = new ol.control.MousePosition({
    coordinateFormat: ol.coordinate.createStringXY(4),
    projection: 'EPSG:3857'
});
map.addControl(MousePosition);

var geolocation = new ol.Geolocation({
    projection: map.getView().getProjection(),
    tracking: true
});

var marker = new ol.Overlay({
    element: document.getElementById('location'),
    positioning: 'center-center'
});

var clicked_coord;
var interaction;
var onSingleClick = function(evt) {
    var coord = evt.coordinate;
    clicked_coord = evt.coordinate
    marker.setPosition(coord);
    console.log(coord)
    var features =sectors.getFeatures();
    document.getElementById("X").value = 0;
    document.getElementById("Y").value = 0;
    var str = "Not in New York"
    for(x in features) {
        var props = features[x].getProperties();
        if (props.geometry.intersectsCoordinate(coord))  str = props['sct_text']
        
    }
    
    if (str != "Not in New York"){
        var closestStation = station.getClosestFeatureToCoordinate(coord)
        console.log(closestStation.getProperties()); 
        document.getElementById("X").value = coord[0];
        document.getElementById("Y").value = coord[1];
        str ='sector: ' + str + '<br/>';
        str = str + "Closest Police Station: " + closestStation.getProperties()['address'] + '<br/>';
        str = str + "Zip code: " + closestStation.getProperties()['zipcode'] + '<br/>'; 

    }

   
    if(str) {
        str = '<p>' + str + '</p>';
        overlayPopup.setPosition(clicked_coord);
        content.innerHTML = str;
        container.style.display = 'block';
    }
    else{
        container.style.display = 'none';
        closer.blur();
    }
    
}

map.on('singleclick', function (evt) {
            onSingleClick(evt);
});


function zoomToMyPosition (){
    map.getView().setCenter(geolocation.getPosition());
    map.getView().setZoom(15);
    console.log(geolocation.getPosition())//getting My location
    marker.setPosition(geolocation.getPosition());
    document.getElementById("X").value = geolocation.getPosition()[0];
    document.getElementById("Y").value = geolocation.getPosition()[1];
}

map.addOverlay(marker);

function goToFullExtent() {
    map.getView().fit(
        map.getView().calculateExtent(),
    );
    map.getView().setZoom(10)

}




   







