document.addEventListener('DOMContentLoaded', function () {

    if (!document.getElementById('home-container')) return;

    function loadHome() {
        fetch('/api/home/')
            .then(r => r.json())
            .then(data => {

                const container = document.getElementById('home-container');
                if (!container) return;

                container.innerHTML = '';

                data.items.forEach(item => {
                    container.innerHTML += `
                        <div class="card p-3 mb-3">
                            <a href="/topic/${item.id}/">
                                <strong>${item.title}</strong>
                            </a>
                            <div class="small text-muted mt-2">
                                ${item.updated}
                            </div>
                        </div>
                    `;
                });
            });
    }

    loadHome();
    setInterval(loadHome, 10000);
});
