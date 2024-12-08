// static/events_list.js

// Function to fetch and display events based on filters
function applyFilters() {
    const keyword = document.getElementById('keyword').value;
    const month = document.getElementById('month').value;
    const order = document.getElementById('order').value;

    const url = new URL('/events_list/api/filter', window.location.origin);
    if (keyword) url.searchParams.append('keyword', keyword);
    if (month) url.searchParams.append('month', month);
    if (order) url.searchParams.append('order', order);

    fetch(url)
        .then(response => response.json())
        .then(events => {
            const eventsList = document.getElementById('eventsList');
            eventsList.innerHTML = ""; // Clear previous content

            if (events.length === 0) {
                eventsList.innerHTML = "<p>No events match your criteria.</p>";
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
                    <p><strong>Points:</strong> ${event.points}</p>
                    <p><strong>Tags:</strong> ${tags}</p>
                `;

                eventsList.appendChild(eventDiv);
            });
        })
        .catch(error => {
            console.error('Error fetching events:', error);
            const eventsList = document.getElementById('eventsList');
            eventsList.innerHTML = "<p>Error loading events. Please try again later.</p>";
        });
}

// Fetch and display all events on page load
document.addEventListener('DOMContentLoaded', function() {
    applyFilters();
});
