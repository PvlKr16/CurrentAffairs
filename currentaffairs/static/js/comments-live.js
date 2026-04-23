document.addEventListener('DOMContentLoaded', function () {

    if (!window.TOPIC_ID) return;

    let lastCount = 0;

    function loadComments() {
        fetch(`/topic/${window.TOPIC_ID}/comments-json/`)
            .then(r => r.json())
            .then(data => {

                if (data.comments.length === lastCount) return;

                lastCount = data.comments.length;

                const container = document.getElementById('comments-container');
                if (!container) return;

                container.innerHTML = '';

                data.comments.forEach(c => {
                    container.innerHTML += `
                        <div class="card mb-3 p-3">
                            <div class="d-flex justify-content-between">
                                <strong>${c.author}</strong>
                                <small>${c.created_at}</small>
                            </div>
                            <div>${c.content}</div>
                        </div>
                    `;
                });
            });
    }

    loadComments();
    setInterval(loadComments, 5000);
});