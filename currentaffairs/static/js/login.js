// Toggle password visibility
document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.getElementById("togglePassword");
    const password = document.getElementById("password");

    toggle.addEventListener("click", function () {
        if (password.type === "password") {
            password.type = "text";
            toggle.innerText = "Hide";
        } else {
            password.type = "password";
            toggle.innerText = "Show";
        }
    });
});
