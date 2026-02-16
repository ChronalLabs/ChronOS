console.log("EcoTrack Loaded");


document.addEventListener("DOMContentLoaded", function () {

    const canvas = document.getElementById("carbonChart");

    if (canvas) {

        const travel = parseFloat(canvas.dataset.travel);
        const electricity = parseFloat(canvas.dataset.electricity);
        const diet = parseFloat(canvas.dataset.diet);

        new Chart(canvas, {
            type: 'bar',
            data: {
                labels: ['Travel', 'Electricity', 'Diet'],
                datasets: [{
                    label: 'CO2 Emissions (kg)',
                    data: [travel, electricity, diet]
                }]
            },
            options: {
                responsive: true
            }
        });
    }
});

