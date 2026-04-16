document.addEventListener('DOMContentLoaded', function () {

    if (!window.POLL_ID) return;

    loadResults();
    setInterval(loadResults, 15000);

});


function loadResults() {

    fetch(`/poll/${window.POLL_ID}/results/`)
        .then(response => response.json())
        .then(data => {

            let total = 0;

            data.results.forEach(item => {
                total += item.count;
            });

            data.results.forEach(item => {

                const row = document.querySelector(
                    `.result-item[data-id="${item.id}"]`
                );

                if (!row) return;

                const count = row.querySelector('.result-count');
                const bar = row.querySelector('.progress-bar');

                count.textContent = item.count;

                const percent = total > 0
                    ? (item.count / total) * 100
                    : 0;

                bar.style.width = percent + '%';
                bar.textContent = Math.round(percent) + '%';
            });

            // Completed
            const badge = document.getElementById('poll-status');

            if (data.completed) {
                badge.classList.remove('d-none');
            }

            // Waiting list
            const waitingBox = document.getElementById('waiting-list');

            if (!data.completed) {
                waitingBox.innerHTML = '';

                data.waiting.forEach(user => {
                    waitingBox.innerHTML +=
                        user[0] + ' ' + user[1] + '<br>';
                });
            } else {
                waitingBox.innerHTML = 'Everyone voted';
            }

            // Anonymous
            if (data.anonymous) {
                document.querySelector('#waiting-box h6')
                    .textContent = 'Anonymous poll';
            }

        });
}
