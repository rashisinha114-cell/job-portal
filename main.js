document.addEventListener("DOMContentLoaded", function () {

    // REGISTER FORM
    const registerForm = document.getElementById("registerForm");

    if (registerForm) {
        registerForm.addEventListener("submit", function (e) {
            e.preventDefault();

            fetch("/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: document.getElementById("username").value,
                    email: document.getElementById("email").value,
                    password: document.getElementById("password").value
                })
            })
            .then(res => res.json())
            .then(data => {
                alert("Registration Successful!");
                window.location.href = "/login-page";
            });
        });
    }

});
