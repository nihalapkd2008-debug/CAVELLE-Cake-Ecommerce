/* =========================================
   CAVELLE FRONTEND
========================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log(
            "CAVELLE frontend loaded successfully."
        );


        /* =====================================
           REGISTER
        ===================================== */

        const registerForm =
            document.getElementById("registerForm");


        if (registerForm) {

            registerForm.addEventListener(
                "submit",
                async function (event) {

                    event.preventDefault();


                    const username =
                        document.getElementById(
                            "username"
                        ).value;

                    const email =
                        document.getElementById(
                            "email"
                        ).value;

                    const phone =
                        document.getElementById(
                            "phone"
                        ).value;

                    const password =
                        document.getElementById(
                            "password"
                        ).value;


                    const message =
                        document.getElementById(
                            "registerMessage"
                        );


                    try {

                        const response =
                            await fetch(
                                "/api/users/register/",
                                {
                                    method: "POST",

                                    headers: {
                                        "Content-Type":
                                            "application/json"
                                    },

                                    body: JSON.stringify({
                                        username:
                                            username,

                                        email:
                                            email,

                                        phone:
                                            phone,

                                        password:
                                            password
                                    })
                                }
                            );


                        const data =
                            await response.json();


                        if (response.ok) {

                            message.textContent =
                                "Account created successfully!";

                            message.className =
                                "form-message success";


                            setTimeout(
                                function () {

                                    window.location.href =
                                        "/login/";

                                },
                                1000
                            );

                        } else {

                            message.textContent =
                                getErrorMessage(data);

                            message.className =
                                "form-message error";
                        }


                    } catch (error) {

                        message.textContent =
                            "Something went wrong. Please try again.";

                        message.className =
                            "form-message error";

                    }

                }
            );

        }


        /* =====================================
           LOGIN
        ===================================== */

        const loginForm =
            document.getElementById("loginForm");


        if (loginForm) {

            loginForm.addEventListener(
                "submit",
                async function (event) {

                    event.preventDefault();


                    const username =
                        document.getElementById(
                            "username"
                        ).value;

                    const password =
                        document.getElementById(
                            "password"
                        ).value;


                    const message =
                        document.getElementById(
                            "loginMessage"
                        );


                    try {

                        const response =
                            await fetch(
                                "/api/token/",
                                {
                                    method: "POST",

                                    headers: {
                                        "Content-Type":
                                            "application/json"
                                    },

                                    body: JSON.stringify({

                                        username:
                                            username,

                                        password:
                                            password

                                    })
                                }
                            );


                        const data =
                            await response.json();


                        if (response.ok) {

                            localStorage.setItem(
                                "access_token",
                                data.access
                            );


                            localStorage.setItem(
                                "refresh_token",
                                data.refresh
                            );


                            message.textContent =
                                "Login successful!";

                            message.className =
                                "form-message success";


                            setTimeout(
                                function () {

                                    window.location.href =
                                        "/products/";

                                },
                                700
                            );

                        } else {

                            message.textContent =
                                "Invalid username or password.";

                            message.className =
                                "form-message error";

                        }


                    } catch (error) {

                        message.textContent =
                            "Something went wrong. Please try again.";

                        message.className =
                            "form-message error";

                    }

                }
            );

        }

    }
);


/* =========================================
   ERROR MESSAGE HELPER
========================================= */

function getErrorMessage(data) {

    if (data.username) {
        return data.username[0];
    }

    if (data.email) {
        return data.email[0];
    }

    if (data.password) {
        return data.password[0];
    }

    if (data.detail) {
        return data.detail;
    }

    return "Unable to create account.";

}