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
