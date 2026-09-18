from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CakeViewSet,
    product_list,
    product_detail,
)


router = DefaultRouter()

router.register(
    "categories",
    CategoryViewSet
)

router.register(
    "cakes",
    CakeViewSet
)


urlpatterns = router.urls + [
    path(
        "shop/",
        product_list,
        name="product-list"
    ),

    path(
        "shop/<int:cake_id>/",
        product_detail,
        name="product-detail"
    ),
]