document.addEventListener("DOMContentLoaded", function () {
    // Initialize Map centering on India
    var map = L.map('map').setView([22.9734, 78.6569], 5);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    var marker;

    map.on('click', function (e) {
        var lat = e.latlng.lat.toFixed(6);
        var lng = e.latlng.lng.toFixed(6);

        if (marker) {
            map.removeLayer(marker);
        }

        marker = L.marker([lat, lng]).addTo(map);

        document.getElementById("lat").innerText = lat;
        document.getElementById("lng").innerText = lng;

        // Call Weather API
        fetchWeather(lat, lng);
    });
});

function fetchWeather(lat, lng) {
    fetch("/get-weather", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ lat: lat, lng: lng })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Weather fetch failed.");
            return;
        }
    
        // Process data for dashboard
        let tempVal = parseFloat(data.temperature) || 0;
        let humVal = parseFloat(data.humidity) || 0;
        let rainVal = data.rain_chance || (data.rain ? 60 : 15);
        
        // Calculate percentages for CSS Gradients
        let tempProgress = Math.min(Math.max(tempVal, 0), 50) * 2; // 0-50°C scale
        
        document.getElementById("weather-info").innerHTML = `
        <div class="climate-dashboard">
            <div class="climate-header text-center">
                <h5>${data.city || 'Farm Location'}</h5>
                <p class="text-capitalize">${data.description}</p>
            </div>
        
            <div class="climate-main">
                <div class="gauge-wrapper text-center ${tempVal > 35 ? 'hot-glow' : ''}">
                    <div class="gauge" style="--percent:${tempProgress}">
                        <div class="gauge-inner">
                            <span class="fw-bold fs-4" data-target="${tempVal}">0</span>
                            <small>°C</small>
                        </div>
                    </div>
                    <label class="d-block mt-2 text-muted">Temperature</label>
                </div>
        
                <div class="humidity-wrapper text-center">
                    <div class="humidity-bar mx-auto">
                        <div class="humidity-fill" style="height:${humVal}%"></div>
                    </div>
                    <span class="fw-bold d-block mt-2" data-target="${humVal}">0</span>
                    <small class="text-muted">Humidity %</small>
                </div>
        
                <div class="rain-wrapper text-center">
                    <div class="rain-ring" style="--rain:${rainVal}">
                        <div class="rain-inner">
                            <span class="fw-bold fs-4" data-target="${rainVal}">0</span>
                            <small>%</small>
                        </div>
                    </div>
                    <label class="d-block mt-2 text-muted">Rain Chance</label>
                </div>
            </div>
        
            <div class="wind-box mx-auto" style="max-width: 200px;">
                <span class="fw-bold fs-5" data-target="${data.wind_speed || 0}">0</span>
                <small class="d-block text-muted">m/s Wind Speed</small>
            </div>

            <div class="crop-panel">
    <h6>🌾 Recommended Crops</h6>
    <div class="crop-tags">
        ${data.recommended_crops.map(crop => 
            `<span class="crop-tag">${crop}</span>`
        ).join("")}
    </div>

    <div class="advice-box">
        <strong>Advisory:</strong>
        <p>${data.advice}</p>
    </div>

    <div class="risk-badge risk-${data.risk.toLowerCase()}">
        Risk Level: ${data.risk}
    </div>
</div>

        </div>
        `;

        animateCounters();
    })
    .catch(error => console.error("Error:", error));
}

function animateCounters() {
    document.querySelectorAll("[data-target]").forEach(el => {
        const target = parseFloat(el.getAttribute("data-target"));
        const duration = 1500; 
        const start = 0;
        let startTime = null;

        function animation(currentTime) {
            if (startTime === null) startTime = currentTime;
            const timeElapsed = currentTime - startTime;
            const progress = Math.min(timeElapsed / duration, 1);
            
            const currentNumber = progress * (target - start) + start;
            el.innerHTML = target % 1 === 0 ? Math.floor(currentNumber) : currentNumber.toFixed(1);

            if (timeElapsed < duration) {
                requestAnimationFrame(animation);
            } else {
                el.innerHTML = target;
            }
        }
        requestAnimationFrame(animation);
    });
}