document.addEventListener("DOMContentLoaded", () => {
    // Example chart: Score trends across semesters
    new Chart(document.getElementById("scoreTrendChart"), {
        type: "line",
        data: {
            labels: courseSemesters, // passed from backend
            datasets: [{
                label: "Average Score",
                data: courseScores,
                borderColor: "#3498DB",
                backgroundColor: "rgba(52,152,219,0.2)",
                tension: 0.3,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true, suggestedMax: 100 }
            }
        }
    });
});
