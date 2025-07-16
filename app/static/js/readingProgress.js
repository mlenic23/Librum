let readingChart = null;

function openReadingModal(bookId, bookTitle, totalPages) {
    document.getElementById('modalBookId').value = bookId;
    document.getElementById('modalBookTitle').innerText = bookTitle;
    document.getElementById('readingModal').style.display = 'block';

    fetch(`/books/${bookId}/progress-data/`)
        .then(res => res.json())
        .then(data => updateReadingProgressChart(data.progress, totalPages))
        .catch(err => console.error('Progress fetch error:', err));
}

function closeReadingModal() {
    document.getElementById('readingModal').style.display = 'none';
    if (readingChart) {
        readingChart.destroy();
        readingChart = null;
    }
}

function updateReadingProgressChart(progressData, totalPages) {
    const ctx = document.getElementById('readingProgressChart').getContext('2d');
    if (readingChart) readingChart.destroy();

    const labels = progressData.map(e => e.date);
    const data = progressData.map(e => e.pages_read);
    const total = data.reduce((a, b) => a + b, 0);

    readingChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: 'Pages Read',
                data,
                borderColor: 'rgba(75,192,192,1)',
                fill: false
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true, max: totalPages, title: { display: true, text: 'Pages' } },
                x: { title: { display: true, text: 'Date' } }
            },
            plugins: {
                title: {
                    display: true,
                    text: `Reading Progress (${total}/${totalPages} pages)`
                }
            }
        }
    });
}

document.getElementById('readingProgressForm').addEventListener('submit', e => {
    e.preventDefault();
    const bookId = document.getElementById('modalBookId').value;
    const pagesRead = document.getElementById('pagesRead').value;

    fetch(`/books/${bookId}/log-progress/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ pages_read: pagesRead })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            if (data.book_completed) {
                alert('Book completed!');
                window.location.reload();
            } else {
                updateReadingProgressChart(data.progress, data.total_pages);
            }
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(err => console.error('Submit error:', err));
});

function getCookie(name) {
    let cookieValue = null;
    document.cookie.split(';').forEach(cookie => {
        const [k, v] = cookie.trim().split('=');
        if (k === name) cookieValue = decodeURIComponent(v);
    });
    return cookieValue;
}

window.onclick = function(event) {
    if (event.target === document.getElementById('readingModal')) {
        closeReadingModal();
    }
};
