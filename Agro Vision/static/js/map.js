// ================= GLOBAL VARIABLES =================
let map;
let marker;
let tempChart = null;
let rainChart = null;

// ================= INITIALIZE MAP =================
document.addEventListener("DOMContentLoaded", function () {

    // Prevent "Map container already initialized" error
    const mapContainer = L.DomUtil.get("map");
    if (mapContainer !== null) {
        mapContainer._leaflet_id = null;
    }

    // Create Map
    map = L.map("map").setView([20.5937, 78.9629], 5); // Default: India

    // Tile Layer
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors"
    }).addTo(map);

    // Click Event
    map.on("click", function (e) {

        const lat = e.latlng.lat.toFixed(4);
        const lng = e.latlng.lng.toFixed(4);

        // Update UI
        document.getElementById("lat").innerText = lat;
        document.getElementById("lng").innerText = lng;

        // Remove old marker
        if (marker) {
            map.removeLayer(marker);
        }

        // Add new marker
        marker = L.marker([lat, lng]).addTo(map);

        // Fetch forecast data
        fetchForecast(lat, lng);
    });

});


// ================= FETCH FORECAST =================
function fetchForecast(lat, lng) {

    fetch("/get-forecast", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ lat: lat, lng: lng })
    })
    .then(response => response.json())
    .then(data => {

        if (!data.labels || !data.temps || !data.rain) {
            console.error("Invalid forecast data format");
            return;
        }

        renderTempChart(data.labels, data.temps);
        renderRainChart(data.labels, data.rain);

    })
    .catch(error => {
        console.error("Forecast error:", error);
    });
}


// ================= TEMPERATURE CHART =================
function renderTempChart(labels, temps) {

    const canvas = document.getElementById("tempChart");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    if (tempChart) {
        tempChart.destroy();
    }

    tempChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Temperature (°C)",
                data: temps,
                borderColor: "#2e7d32",
                backgroundColor: "rgba(46,125,50,0.15)",
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 1200
            },
            plugins: {
                legend: {
                    labels: {
                        font: {
                            weight: "bold"
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}


// ================= RAINFALL CHART =================
function renderRainChart(labels, rain) {

    const canvas = document.getElementById("rainChart");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    if (rainChart) {
        rainChart.destroy();
    }

    rainChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Rainfall Probability (%)",
                data: rain,
                backgroundColor: "rgba(189, 239, 26, 0.7)",
                borderRadius: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 1200
            },
            plugins: {
                legend: {
                    labels: {
                        font: {
                            weight: "bold"
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}
