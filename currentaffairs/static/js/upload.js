document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('upload-form');
    const zone = document.getElementById('drop-zone');
    const preview = document.getElementById('preview-box');

    if (!form || !zone) return;

    const input = form.querySelector('input[type="file"]');
    if (!input) return;

    zone.addEventListener('click', () => input.click());

    zone.addEventListener('dragover', function (e) {
        e.preventDefault();
        zone.classList.add('dragover');
    });

    zone.addEventListener('dragleave', function () {
        zone.classList.remove('dragover');
    });

    zone.addEventListener('drop', function (e) {
        e.preventDefault();
        zone.classList.remove('dragover');

        const file = e.dataTransfer.files[0];
        if (!file) return;

        input.files = e.dataTransfer.files;
        renderPreview(file);
    });

    input.addEventListener('change', function () {
        const file = input.files[0];
        if (file) renderPreview(file);
    });

    function renderPreview(file) {

        preview.innerHTML = '';

        if (file.size > 5 * 1024 * 1024) {
            preview.innerHTML =
                '<div class="text-danger">Max 5 MB</div>';
            input.value = '';
            return;
        }

        const size =
            (file.size / 1024).toFixed(1) + ' KB';

        if (file.type.startsWith('image/')) {

            const img = document.createElement('img');
            img.className = 'img-thumbnail mt-2';
            img.style.maxWidth = '180px';

            img.src = URL.createObjectURL(file);

            preview.appendChild(img);
        }

        preview.innerHTML +=
            `<div class="small mt-2">${file.name} (${size})</div>`;
    }

});
