document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-set-theme]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const theme = this.dataset.setTheme;
            document.documentElement.setAttribute('data-theme', theme);
        });
    });
});
