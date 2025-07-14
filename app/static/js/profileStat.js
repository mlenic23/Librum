document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('pagesChart').getContext('2d');
    const pagesToday = parseInt("{{ pages_today|default:'0' }}"); // Dinamički podaci iz template-a

    const pagesChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Danas'],
            datasets: [{
                label: 'Pročitano stranica',
                data: [pagesToday],
                backgroundColor: 'rgba(78, 47, 26, 0.8)',
                borderColor: 'rgba(78, 47, 26, 1)',
                borderWidth: 1,
                barThickness: 50
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Broj stranica' },
                    ticks: { stepSize: 10 }
                }
            },
            plugins: {
                legend: { display: false }
            },
            responsive: true,
            maintainAspectRatio: false
        }
    });
});