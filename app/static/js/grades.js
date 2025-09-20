// Mini radar chart for insights
new Chart(document.getElementById("insightsChart"), {
    type: "radar",
    data: {
        labels: {{ [c.name for c in scores]| tojson }},
    datasets: [{
        label: "Scores",
        data: {{ [c.score for c in scores] | tojson }},
    backgroundColor: "rgba(52,152,219,0.2)",
    borderColor: "#3498DB",
    pointBackgroundColor: "#3498DB"
    }]
  },
    options: { responsive: true, scales: { r: { beginAtZero: true, max: 100 } } }
});
