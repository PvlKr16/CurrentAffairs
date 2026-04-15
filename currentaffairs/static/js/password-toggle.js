document.addEventListener('DOMContentLoaded', function () {

    // Always hide all warnings on page load
    document.querySelectorAll('.caps-warning').forEach(function (el) {
        el.classList.add('d-none');
    });

    // Hold to show password
    document.querySelectorAll('.password-peek').forEach(function (btn) {

        const wrapper = btn.closest('.password-wrapper');
        if (!wrapper) return;

        const input = wrapper.querySelector('input');
        if (!input) return;

        const show = () => input.type = 'text';
        const hide = () => input.type = 'password';

        btn.addEventListener('mousedown', show);
        btn.addEventListener('mouseup', hide);
        btn.addEventListener('mouseleave', hide);

        btn.addEventListener('touchstart', show);
        btn.addEventListener('touchend', hide);
    });

    // Caps Lock warning
    document.querySelectorAll('.password-wrapper input').forEach(function (input) {

        const container = input.closest('.mb-3');
        if (!container) return;

        const warning = container.querySelector('.caps-warning');
        if (!warning) return;

        function checkCaps(e) {
            const caps = e.getModifierState && e.getModifierState('CapsLock');

            if (caps) {
                warning.classList.remove('d-none');
            } else {
                warning.classList.add('d-none');
            }
        }

        input.addEventListener('keydown', checkCaps);
        input.addEventListener('keyup', checkCaps);
        input.addEventListener('blur', function () {
            warning.classList.add('d-none');
        });
    });

    // Password strength
    const newPass = document.querySelector('input[name="new_password1"]');

    if (newPass) {
        const container = newPass.closest('.mb-3');
        const bar = container.querySelector('.strength-bar');
        const text = container.querySelector('.strength-text');

        newPass.addEventListener('input', function () {

            if (!bar || !text) return;

            const val = newPass.value;
            let score = 0;

            if (val.length >= 8) score++;
            if (/[A-Z]/.test(val)) score++;
            if (/[a-z]/.test(val)) score++;
            if (/[0-9]/.test(val)) score++;
            if (/[^A-Za-z0-9]/.test(val)) score++;

            const labels = ['Empty', 'Weak', 'Fair', 'Good', 'Strong', 'Excellent'];
            const widths = ['0%', '20%', '40%', '60%', '80%', '100%'];

            bar.style.width = widths[score];
            bar.className = 'strength-bar level-' + score;
            text.textContent = labels[score];
        });
    }

});
