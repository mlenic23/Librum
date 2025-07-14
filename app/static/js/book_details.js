document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('reviewModal');
    const openBtn = document.getElementById('openReviewModal');
    const closeBtn = document.getElementById('closeModal');

    openBtn.addEventListener('click', function () {
        modal.classList.add('active');
        document.body.classList.add('modal-active');
    });

    closeBtn.addEventListener('click', function () {
        modal.classList.remove('active');
        document.body.classList.remove('modal-active');
    });

    window.addEventListener('click', function (e) {
        if (e.target === modal) {
            modal.classList.remove('active');
            document.body.classList.remove('modal-active');
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const summaryModal = document.getElementById('summaryModal');
    const openSummaryBtn = document.getElementById('openSummaryModal');
    const closeSummaryBtn = document.getElementById('closeSummaryModal');

    openSummaryBtn.addEventListener('click', function () {
        summaryModal.classList.add('active');
        document.body.classList.add('modal-active');
    });

    closeSummaryBtn.addEventListener('click', function () {
        summaryModal.classList.remove('active');
        document.body.classList.remove('modal-active');
    });

    window.addEventListener('click', function (e) {
        if (e.target === summaryModal) {
            summaryModal.classList.remove('active');
            document.body.classList.remove('modal-active');
        }
    });
});

function submitRating() {
    document.getElementById('ratingForm').submit();
}

document.querySelectorAll('.action-icon').forEach(icon => {
    icon.addEventListener('click', function(e) {
        e.preventDefault();
        const url = this.getAttribute('href');
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                this.classList.toggle('filled');
            }
        })
        .catch(error => console.error('Error:', error));
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const currentlyReadingForm = document.querySelector('form[action^="/add_to_currently_reading/"]');
    if (currentlyReadingForm) {
        currentlyReadingForm.addEventListener('submit', function(e) {
            e.preventDefault(); 

            const bookId = currentlyReadingForm.action.split('/').pop();
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/add_to_currently_reading/${bookId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken,
                },
                body: `csrfmiddlewaretoken=${csrfToken}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Book added to Currently Reading!');
                    window.location.href = '/auth/profile/'; // Preusmjeravanje na profil
                } else {
                    alert(data.error || 'Failed to add book.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Check console for details.');
            });
        });
    }
});