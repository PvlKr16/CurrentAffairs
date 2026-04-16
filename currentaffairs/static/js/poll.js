document.addEventListener('DOMContentLoaded', function () {

    const btn = document.getElementById('add-option');
    const box = document.getElementById('options-container');

    if (!btn || !box) return;

    btn.addEventListener('click', function () {
        const input = document.createElement('input');

        input.type = 'text';
        input.name = 'options';
        input.className = 'form-control mb-2';

        box.appendChild(input);
    });

});
