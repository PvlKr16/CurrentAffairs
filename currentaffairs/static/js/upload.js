document.addEventListener('DOMContentLoaded', function () {
    let lang = document.documentElement.getAttribute('lang') || 'en';
    lang = lang.slice(0, 2).toLowerCase();

    const i18n = {
        be: { choose: 'Выберыце файл', empty: 'Файл не выбраны' },
        en: { choose: 'Choose file', empty: 'No file selected' },
        it: { choose: 'Scegli file', empty: 'Nessun file selezionato' },
        lt: { choose: 'Pasirinkti failą', empty: 'Failas nepasirinktas' },
        ru: { choose: 'Выберите файл', empty: 'Файл не выбран' },
        ua: { choose: 'Оберіть файл', empty: 'Файл не вибрано' }
    };

    const t = i18n[lang] || i18n.en;

    document.querySelectorAll('input[type="file"]').forEach(input => {
        if (input.dataset.ready) return;
        input.dataset.ready = '1';

        input.classList.add('d-none');

        const wrap = document.createElement('div');
        wrap.className = 'd-flex align-items-center gap-2';

        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'btn btn-outline-secondary btn-sm';
        btn.textContent = t.choose;

        const label = document.createElement('span');
        label.className = 'small text-muted';
        label.textContent = t.empty;

        input.parentNode.insertBefore(wrap, input);
        wrap.appendChild(btn);
        wrap.appendChild(label);
        wrap.appendChild(input);

        btn.addEventListener('click', () => input.click());

        input.addEventListener('change', function () {
            label.textContent = input.files.length
                ? input.files[0].name
                : t.empty;
        });
    });
});
