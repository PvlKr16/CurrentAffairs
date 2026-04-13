document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('search-input');
    const panel = document.getElementById('search-panel');

    if (!input || !panel) return;

    input.addEventListener('focus', function () {
        panel.classList.remove('d-none');
    });

    document.addEventListener('click', function (e) {
        if (!panel.contains(e.target) && e.target !== input) {
            panel.classList.add('d-none');
        }
    });
});
