// static/map.js

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
            // Remove existing markers
            map.eachLayer(layer => {
                if (layer.options && layer.options.pane === "markerPane") {
                    map.removeLayer(layer);
                }
            });

            // Add new markers
            events.forEach(event => {
                const [lat, lng] = event.location.split(',').map(Number);
                L.marker([lat, lng]).addTo(map)
                    .bindPopup(`<strong>${event.name}</strong><br>${event.description}<br>${event.date}`);
            });

            // Update Event List
            updateEventList(events);
        })
        .catch(error => console.error('Error fetching events:', error));
}

// Update Month
function updateMonth(value) {
    const month = parseInt(value);
    document.getElementById('selectedMonth').textContent = monthNames[month - 1];
    fetchAndDisplayEvents(month);
}

// Update Event List
function updateEventList(events) {
    const eventList = document.getElementById('eventList');
    eventList.innerHTML = ""; // Clear previous content

    if (events.length === 0) {
        eventList.innerHTML = "<p>No events to display for the selected month.</p>";
        return;
    }

    events.forEach(event => {
        const eventDiv = document.createElement('div');
        eventDiv.className = "event";
        if (event.recommended) {
            eventDiv.classList.add("recommended");
        }

        const tags = event.tags.length > 0 ? event.tags.join(', ') : "No tags";

        eventDiv.innerHTML = `
            <h3><a href="/home/event/${event.id}">${event.name}</a></h3>
            <p><strong>Date:</strong> ${event.date}</p>
            <p><strong>Open Slots:</strong> ${event.openslots}</p>
            <p><strong>Tags:</strong> ${tags}</p>
        `;

        eventList.appendChild(eventDiv);
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', initMap);
