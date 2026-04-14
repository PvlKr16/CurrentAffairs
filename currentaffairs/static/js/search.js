document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('search-input');
    const panel = document.getElementById('search-panel');
    const dateToggle = document.getElementById('date-toggle');
    const dateRange = document.getElementById('date-range');

    if (!input || !panel) return;

    input.addEventListener('focus', function () {
        panel.classList.remove('d-none');
    });

    document.addEventListener('click', function (e) {
        if (!panel.contains(e.target) && e.target !== input) {
            panel.classList.add('d-none');
        }
    });

    if (dateToggle && dateRange) {
        dateToggle.addEventListener('change', function () {
            if (this.checked) {
                dateRange.classList.remove('d-none');
            } else {
                dateRange.classList.add('d-none');
            }
        });
    }
});
