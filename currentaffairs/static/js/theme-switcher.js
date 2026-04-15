document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.theme-option');

    buttons.forEach(function (button) {
        button.addEventListener('click', function (e) {
            e.preventDefault();

            const theme = this.dataset.theme;
            if (!theme) return;

            // Instant UI update
            document.documentElement.setAttribute('data-theme', theme);

            // Save in DB
            fetch('/change-theme/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                },
                body: new URLSearchParams({
                    theme: theme
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status !== 'ok') {
                    console.error('Theme save failed');
                }
            })
            .catch(error => {
                console.error('Theme request error:', error);
            });
        });
    });
});


function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split(';') : [];

    for (let cookie of cookies) {
        cookie = cookie.trim();

        if (cookie.startsWith(name + '=')) {
            return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }

    return null;
}
