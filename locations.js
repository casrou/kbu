export { clearMarkers, addMapMarker };

var map = new maplibregl.Map({
  container: "map", // container id
  style:
    "https://api.maptiler.com/maps/basic-v2/style.json?key=4oZhY3NiUFERNYdnnM6t", // style URL
  center: [10.8, 56], // starting position [lng, lat]
  zoom: 6.5, // starting zoom
});

var markers = [];

async function fetchLocations() {
  return fetch("locations.json").then((r) => r.json());
}

async function addMapMarker(enhed) {
  let locations = await fetchLocations();
  let location = locations.find((e) => e.enhed === enhed).result.places[0];
  console.debug(location);

  const popup = new maplibregl.Popup({}).setText(enhed);

  let marker = new maplibregl.Marker({ color: "#33333390" })
    .setLngLat([location.location.longitude, location.location.latitude])
    .setPopup(popup)
    .addTo(map);
  markers.push(marker);
}

function clearMarkers() {
  markers.forEach((m) => m.remove());
}
