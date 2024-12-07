let map;
const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
];

// Initialize Map
function initMap() {
    map = L.map('map').setView([44.4268, 26.1025], 12); // Bucharest coordinates
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
    }).addTo(map);
    fetchAndDisplayEvents(1); // Default month: January
}

// Fetch Events from Server
function fetchAndDisplayEvents(month) {
    fetch(`/home/events?month=${month}`)
        .then(response => response.json())
        .then(events => {
            map.eachLayer(layer => {
                if (layer.options && layer.options.pane === "markerPane") {
                    map.removeLayer(layer); // Remove existing markers
                }
            });

            events.forEach(event => {
                const [lat, lng] = event.location.split(',').map(Number);
                L.marker([lat, lng]).addTo(map)
                    .bindPopup(`<strong>${event.name}</strong><br>${event.description}<br>${event.date}`);
            });
        })
        .catch(error => console.error('Error fetching events:', error));
}

// Update Month
function updateMonth(value) {
    const month = parseInt(value);
    document.getElementById('selectedMonth').textContent = monthNames[month - 1];
    fetchAndDisplayEvents(month);
}

// Initialize
document.addEventListener('DOMContentLoaded', initMap);
