from rest_framework.routers import DefaultRouter

from .views import (
    CartViewSet,
    CartItemViewSet,
    AddressViewSet,
    OrderViewSet,
    OrderItemViewSet,
)

router = DefaultRouter()

router.register("carts", CartViewSet, basename="cart")
router.register("cart-items", CartItemViewSet, basename="cart-item")
router.register("addresses", AddressViewSet, basename="address")
router.register("orders", OrderViewSet, basename="order")
router.register("order-items", OrderItemViewSet, basename="order-item")

urlpatterns = router.urls