const map = L.map('map-container').setView([51.04, 13.72], 6);

// Basemap
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let geojsonData = null;
let currentLayer = null;

// Load GeoJSON and initialize map
(async function () {
    const response = await fetch('NUTS_RG_03M_2024_4326.geojson');
    geojsonData = await response.json();
    console.log('GeoJSON loaded');

    renderLevel(1); // Initial render
    addLevelSelectorControl(); // Add custom dropdown to map
})();

// Render features for a given LEVL_CODE
function renderLevel(level) {
    if (currentLayer) {
        map.removeLayer(currentLayer);
    }

    const filtered = geojsonData.features.filter(f => f.properties.LEVL_CODE == level);

    currentLayer = L.geoJSON(filtered, {
        style: {
            color: "#007bff",
            fillOpacity: 0.3
        },
        onEachFeature: (feature, layer) => {
            const name = feature.properties.NUTS_NAME;
            const id = feature.properties.NUTS_ID;
            layer.bindPopup(`<strong>${name}</strong><br>ID: ${id}`);
        }
    }).addTo(map);
}

// Add dropdown control inside the map
function addLevelSelectorControl() {
    const LevelControl = L.Control.extend({
        options: { position: 'topright' },

        onAdd: function () {
            const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');

            container.style.background = 'white';
            container.style.padding = '5px';

            const label = document.createElement('label');
            label.innerText = 'LEVL_CODE: ';
            label.style.marginRight = '5px';

            const select = document.createElement('select');
            [1, 2, 3].forEach(level => {
                const option = document.createElement('option');
                option.value = level;
                option.textContent = `Level ${level}`;
                select.appendChild(option);
            });

            select.addEventListener('change', function () {
                const level = parseInt(this.value);
                renderLevel(level);
            });

            container.appendChild(label);
            container.appendChild(select);

            L.DomEvent.disableClickPropagation(container);

            return container;
        }
    });

    map.addControl(new LevelControl());
}
