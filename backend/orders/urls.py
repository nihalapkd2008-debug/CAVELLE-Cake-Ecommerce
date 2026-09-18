from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CartViewSet,
    CartItemViewSet,
    AddressViewSet,
    OrderViewSet,
    OrderItemViewSet,
    StaffOrderViewSet,
)


router = DefaultRouter()

router.register(
    "cart",
    CartViewSet,
    basename="cart"
)

router.register(
    "cart-items",
    CartItemViewSet,
    basename="cart-item"
)

router.register(
    "addresses",
    AddressViewSet,
    basename="address"
)

router.register(
    "orders",
    OrderViewSet,
    basename="order"
)

router.register(
    "order-items",
    OrderItemViewSet,
    basename="order-item"
)

router.register(
    "staff/orders",
    StaffOrderViewSet,
    basename="staff-order"
)


urlpatterns = router.urls