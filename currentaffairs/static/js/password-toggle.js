document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll('.toggle-password').forEach(function (button) {

        button.addEventListener('click', function () {

            const wrapper = this.closest('.password-wrapper');
            if (!wrapper) return;

            const input = wrapper.querySelector('input');
            if (!input) return;

            if (input.type === 'password') {
                input.type = 'text';
                this.textContent = 'Hide';
            } else {
                input.type = 'password';
                this.textContent = 'Show';
            }

        });

    });

});
