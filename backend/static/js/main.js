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
            document.getElementById(
                "registerForm"
            );


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
            document.getElementById(
                "loginForm"
            );


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


        /* =====================================
           ADD TO CART
        ===================================== */

        const addToCartForm =
            document.getElementById(
                "addToCartForm"
            );


        if (addToCartForm) {

            addToCartForm.addEventListener(
                "submit",
                async function (event) {

                    event.preventDefault();


                    const token =
                        localStorage.getItem(
                            "access_token"
                        );


                    const message =
                        document.getElementById(
                            "cartMessage"
                        );


                    const cakeId =
                        addToCartForm.dataset.cakeId;


                    const quantity =
                        parseInt(
                            document.getElementById(
                                "quantity"
                            ).value
                        );


                    if (!token) {

                        message.textContent =
                            "Please login to add items to your cart.";

                        message.className =
                            "form-message error";


                        setTimeout(
                            function () {

                                window.location.href =
                                    "/login/";

                            },
                            1000
                        );

                        return;
                    }


                    if (
                        !quantity ||
                        quantity < 1
                    ) {

                        message.textContent =
                            "Please enter a valid quantity.";

                        message.className =
                            "form-message error";

                        return;
                    }


                    try {

                        const response =
                            await fetch(
                                "/api/orders/cart-items/",
                                {
                                    method: "POST",

                                    headers: {

                                        "Content-Type":
                                            "application/json",

                                        "Authorization":
                                            "Bearer " + token

                                    },

                                    body: JSON.stringify({

                                        cake:
                                            cakeId,

                                        quantity:
                                            quantity

                                    })
                                }
                            );


                        const data =
                            await response.json();


                        if (response.ok) {

                            message.textContent =
                                "Cake added to cart successfully!";

                            message.className =
                                "form-message success";


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
           PRODUCT FILTER / SEARCH / SORT
        ===================================== */

        const categoryFilter =
            document.getElementById(
                "categoryFilter"
            );

        const sortFilter =
            document.getElementById(
                "sortFilter"
            );

        const cakeSearch =
            document.getElementById(
                "cakeSearch"
            );

        const productGrid =
            document.getElementById(
                "productGrid"
            );

        const cakeCount =
            document.getElementById(
                "cakeCount"
            );

        const noSearchResults =
            document.getElementById(
                "noSearchResults"
            );


        if (
            categoryFilter &&
            sortFilter &&
            cakeSearch &&
            productGrid
        ) {

            const productCards =
                Array.from(
                    productGrid.querySelectorAll(
                        ".product-card"
                    )
                );


            /* =================================
               GET CATEGORY FROM URL
            ================================= */

            const urlParams =
                new URLSearchParams(
                    window.location.search
                );

            const urlCategory =
                urlParams.get(
                    "category"
                );


            if (urlCategory) {

                categoryFilter.value =
                    urlCategory;

            }


            /* =================================
               APPLY FILTERS
            ================================= */

            function applyProductFilters() {

                const selectedCategory =
                    categoryFilter.value;

                const selectedSort =
                    sortFilter.value;

                const searchText =
                    cakeSearch.value
                        .trim()
                        .toLowerCase();


                let visibleCards = [];


                /* =============================
                   FILTER
                ============================= */

                productCards.forEach(
                    function (card) {

                        const cardCategory =
                            card.dataset.category;

                        const cardName =
                            card.dataset.name;

                        const cardFlavour =
                            card.dataset.flavour;


                        const categoryMatch =
                            selectedCategory === "all" ||
                            cardCategory === selectedCategory;


                        const searchMatch =
                            !searchText ||
                            cardName.includes(
                                searchText
                            ) ||
                            cardFlavour.includes(
                                searchText
                            ) ||
                            cardCategory
                                .toLowerCase()
                                .includes(
                                    searchText
                                );


                        if (
                            categoryMatch &&
                            searchMatch
                        ) {

                            card.style.display =
                                "";

                            visibleCards.push(
                                card
                            );

                        } else {

                            card.style.display =
                                "none";

                        }

                    }
                );


                /* =============================
                   SORT
                ============================= */

                visibleCards.sort(
                    function (a, b) {

                        if (
                            selectedSort ===
                            "price-low"
                        ) {

                            return (
                                parseFloat(
                                    a.dataset.price
                                ) -
                                parseFloat(
                                    b.dataset.price
                                )
                            );

                        }


                        if (
                            selectedSort ===
                            "price-high"
                        ) {

                            return (
                                parseFloat(
                                    b.dataset.price
                                ) -
                                parseFloat(
                                    a.dataset.price
                                )
                            );

                        }


                        if (
                            selectedSort ===
                            "newest"
                        ) {

                            return (
                                parseInt(
                                    b.dataset.created
                                ) -
                                parseInt(
                                    a.dataset.created
                                )
                            );

                        }


                        return 0;

                    }
                );


                /* =============================
                   REORDER CARDS
                ============================= */

                visibleCards.forEach(
                    function (card) {

                        productGrid.appendChild(
                            card
                        );

                    }
                );


                /* =============================
                   COUNT
                ============================= */

                if (cakeCount) {

                    cakeCount.textContent =
                        visibleCards.length +
                        (
                            visibleCards.length === 1
                                ? " Cake"
                                : " Cakes"
                        );

                }


                /* =============================
                   EMPTY SEARCH STATE
                ============================= */

                if (noSearchResults) {

                    if (
                        visibleCards.length === 0 &&
                        productCards.length > 0
                    ) {

                        noSearchResults.style.display =
                            "block";

                    } else {

                        noSearchResults.style.display =
                            "none";

                    }

                }

            }


            /* =================================
               CATEGORY CHANGE
            ================================= */

            categoryFilter.addEventListener(
                "change",
                function () {

                    const selectedCategory =
                        categoryFilter.value;


                    if (
                        selectedCategory ===
                        "all"
                    ) {

                        window.history.replaceState(
                            {},
                            "",
                            "/products/"
                        );

                    } else {

                        const newUrl =
                            "/products/?category=" +
                            encodeURIComponent(
                                selectedCategory
                            );

                        window.history.replaceState(
                            {},
                            "",
                            newUrl
                        );

                    }


                    applyProductFilters();

                }
            );


            /* =================================
               SORT CHANGE
            ================================= */

            sortFilter.addEventListener(
                "change",
                function () {

                    applyProductFilters();

                }
            );


            /* =================================
               SEARCH
            ================================= */

            cakeSearch.addEventListener(
                "input",
                function () {

                    applyProductFilters();

                }
            );


            /* =================================
               INITIAL FILTER
            ================================= */

            applyProductFilters();

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


    if (data.quantity) {
        return data.quantity[0];
    }


    if (data.cake) {
        return data.cake[0];
    }


    if (data.detail) {
        return data.detail;
    }


    return "Something went wrong. Please try again.";

}