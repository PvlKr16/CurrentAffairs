function updateUnreadCounter() {
    fetch('/api/unread-count/')
        .then(response => response.json())
        .then(data => {
            const badge = document.getElementById('unread-badge');

            if (!badge) return;

            if (data.count > 0) {
                badge.innerText = data.count;
                badge.classList.remove('d-none');
            } else {
                badge.classList.add('d-none');
            }
        });
}

document.addEventListener('DOMContentLoaded', function () {
    updateUnreadCounter();
    setInterval(updateUnreadCounter, 10000);
});
