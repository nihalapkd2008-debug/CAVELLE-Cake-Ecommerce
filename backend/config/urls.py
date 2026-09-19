from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    home,
    products_page,
    product_detail,
    login_page,
    register_page,
    cart_page,
    checkout_page,
    orders_page,
    wishlist_page,
    profile_page,
    staff_orders_page,
    bakery_gallery,
)


urlpatterns = [

    # =========================================
    # ADMIN
    # =========================================

    path(
        "admin/",
        admin.site.urls
    ),


    # =========================================
    # FRONTEND PAGES
    # =========================================

    path(
        "",
        home,
        name="home"
    ),

    path(
        "products/",
        products_page,
        name="products"
    ),

    path(
        "products/<int:cake_id>/",
        product_detail,
        name="product-detail"
    ),

    path(
        "login/",
        login_page,
        name="login"
    ),

    path(
        "register/",
        register_page,
        name="register"
    ),

    path(
        "cart/",
        cart_page,
        name="cart"
    ),

    path(
        "checkout/",
        checkout_page,
        name="checkout"
    ),

    path(
        "orders/",
        orders_page,
        name="orders"
    ),

    path(
        "wishlist/",
        wishlist_page,
        name="wishlist"
    ),

    path(
        "profile/",
        profile_page,
        name="profile"
    ),

    path(
        "staff/orders/",
        staff_orders_page,
        name="staff-orders"
    ),


    # =========================================
    # JWT AUTHENTICATION
    # =========================================

    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),


    # =========================================
    # API ROUTES
    # =========================================

    path(
        "api/users/",
        include("users.urls")
    ),

    path(
        "api/products/",
        include("products.urls")
    ),

    path(
        "api/orders/",
        include("orders.urls")
    ),

    path(
        "api/payments/",
        include("payments.urls")
    ),

    path(
        "api/reviews/",
        include("reviews.urls")
    ),


    # =========================================
    # BAKERY GALLERY
    # =========================================

    path(
        "bakery/<int:item_id>/",
        bakery_gallery,
        name="bakery-gallery"
    ),
]


# =========================================
# MEDIA FILES
# =========================================

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)