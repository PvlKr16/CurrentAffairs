document.addEventListener('DOMContentLoaded', function () {

    if (!window.POLL_ID) return;

    loadResults();
    setInterval(loadResults, 5000);

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
                const usersBox = row.querySelector('.vote-users');

                count.textContent = item.count;

                const percent = total > 0
                    ? (item.count / total) * 100
                    : 0;

                bar.style.width = percent + '%';
                bar.textContent = Math.round(percent) + '%';

                // Users list for non-anonymous poll
                usersBox.innerHTML = '';

                if (!data.anonymous && item.users.length > 0) {
                    item.users.forEach(user => {
                        usersBox.innerHTML +=
                            user[0] + ' ' + user[1] + '<br>';
                    });
                }

            });

            const badge = document.getElementById('poll-status');

            if (data.completed) {
                badge.classList.remove('d-none');
            }

            const waitingBox = document.getElementById('waiting-box');
            const waitingList = document.getElementById('waiting-list');

            if (data.completed) {
                waitingBox.style.display = 'none';
            } else {
                waitingBox.style.display = 'block';
                waitingList.innerHTML = '';

                data.waiting.forEach(user => {
                    waitingList.innerHTML +=
                        user[0] + ' ' + user[1] + '<br>';
                });
            }

            if (data.anonymous && !data.completed) {
                const title = waitingBox.querySelector('h6');
                if (title) {
                    title.textContent = 'Anonymous poll';
                }
            }

        });
}
