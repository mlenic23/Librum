document.addEventListener('DOMContentLoaded', function () {

    window.openReadingModal = function(bookId, bookTitle, numberOfPages) {
        document.getElementById("modalBookTitle").innerText = bookTitle;
        document.getElementById("modalBookId").value = bookId;
        document.getElementById("pagesRead").max = numberOfPages;

        fetch(`/books/${bookId}/total-progress/?t=${Date.now()}`)
            .then(response => response.json())
            .then(data => {
                updateProgressBar(data.total_read, numberOfPages);
            });

        document.getElementById("readingModal").style.display = "block";
    }

    window.closeReadingModal = function () {
        document.getElementById("readingModal").style.display = "none";
    }

    function updateProgressBar(pagesRead, totalPages) {
        const percent = Math.min(100, Math.round((pagesRead / totalPages) * 100));
        document.getElementById('progressBar').style.width = `${percent}%`;
        document.getElementById('progressText').innerText = `Read ${pagesRead} of ${totalPages} pages (${percent}%)`;
    }

    const form = document.getElementById('readingProgressForm');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const bookId = document.getElementById('modalBookId').value;
            const pagesRead = document.getElementById('pagesRead').value;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/books/${bookId}/log-progress/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: `pages_read=${pagesRead}&book_id=${bookId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    document.getElementById('pagesRead').value = '';
                    
                    fetch(`/books/${bookId}/total-progress/?t=${Date.now()}`)
                        .then(response => response.json())
                        .then(data => {
                            const totalPages = document.getElementById('pagesRead').max;
                            updateProgressBar(data.total_read, totalPages);
                        });
                } else {
                    alert('Greška: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Došlo je do greške:', error);
            });
        });
    }

});

document.addEventListener('DOMContentLoaded', () => {
  const profileImage = document.getElementById('profileImage');
  const uploadForm = document.getElementById('uploadForm');

  profileImage.addEventListener('click', () => {
    if (uploadForm.style.display === 'block') {
      uploadForm.style.display = 'none';
    } else {
      uploadForm.style.display = 'block';
    }
  });

  document.addEventListener('click', (e) => {
    if (!uploadForm.contains(e.target) && e.target !== profileImage) {
      uploadForm.style.display = 'none';
    }
  });
});
