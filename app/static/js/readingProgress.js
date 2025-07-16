function openReadingModal(bookId, bookTitle, numberOfPages) {
    document.getElementById("modalBookTitle").innerText = bookTitle;
    document.getElementById("modalBookId").value = bookId;
    document.getElementById("pagesRead").max = numberOfPages;

    fetchAndRenderChart(bookId);
    document.getElementById("readingModal").style.display = "block";
}

function closeReadingModal() {
    document.getElementById("readingModal").style.display = "none";
}

function fetchAndRenderChart(bookId) {
    fetch(`/auth/books/${bookId}/progress-chart-data/?t=${Date.now()}`)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('pagesChart').getContext('2d');

            if (window.myChart) {
                window.myChart.destroy();
            }

            window.myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.dates,
                    datasets: [{
                        label: 'Pages read per day',
                        data: data.pages,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        fill: false,
                        tension: 0.1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Pages Read'
                            }
                        }
                    }
                }
            });
        });
}

// AJAX za slanje napretka bez reload-a
document.getElementById('readingProgressForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const bookId = document.getElementById('modalBookId').value;
    const pagesRead = document.getElementById('pagesRead').value;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/auth/books/${bookId}/log-progress/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        },
        body: `pages_read=${pagesRead}&book_id=${bookId}`
    })
    .then(response => {
        if (response.ok) {
            fetchAndRenderChart(bookId);
            document.getElementById('pagesRead').value = '';
        } else {
            alert('Error logging progress.');
        }
    });
});