from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
)
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Category, Cake
from .serializers import CategorySerializer, CakeSerializer

from users.permissions import IsCustomer


# --------------------------------
# PERMISSION
# --------------------------------

class IsStaffOrAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated
            and (
                request.user.role == "staff"
                or request.user.is_superuser
            )
        )


# --------------------------------
# CATEGORY API
# --------------------------------

class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()

    serializer_class = CategorySerializer

    permission_classes = [
        IsStaffOrAdminOrReadOnly
    ]


# --------------------------------
# CAKE API
# --------------------------------

class CakeViewSet(viewsets.ModelViewSet):

    queryset = Cake.objects.select_related(
        "category"
    ).prefetch_related(
        "reviews"
    )

    serializer_class = CakeSerializer

    permission_classes = [
        IsStaffOrAdminOrReadOnly
    ]

    # --------------------------------
    # GET CUSTOMER WISHLIST
    # --------------------------------

    @action(
        detail=False,
        methods=["get"],
        url_path="wishlist",
        permission_classes=[IsCustomer]
    )
    def wishlist_list(self, request):

        cakes = Cake.objects.filter(
            wishlist_users=request.user
        ).select_related(
            "category"
        )

        serializer = self.get_serializer(
            cakes,
            many=True
        )

        return Response(
            serializer.data,
            status=200
        )

    # --------------------------------
    # ADD / REMOVE WISHLIST
    # --------------------------------

    @action(
        detail=True,
        methods=["post", "delete"],
        url_path="wishlist",
        permission_classes=[IsCustomer]
    )
    def wishlist(self, request, pk=None):

        cake = self.get_object()

        # ADD TO WISHLIST
        if request.method == "POST":

            if cake.wishlist_users.filter(
                id=request.user.id
            ).exists():

                raise ValidationError(
                    "Cake is already in your wishlist."
                )

            cake.wishlist_users.add(
                request.user
            )

            return Response(
                {
                    "detail":
                        "Cake added to wishlist."
                },
                status=201
            )

        # REMOVE FROM WISHLIST
        cake.wishlist_users.remove(
            request.user
        )

        return Response(
            {
                "detail":
                    "Cake removed from wishlist."
            },
            status=200
        )


# --------------------------------
# WEBSITE - PRODUCT LIST
# --------------------------------

def product_list(request):

    cakes = Cake.objects.select_related(
        "category"
    ).all()

    return render(
        request,
        "products.html",
        {
            "cakes": cakes
        }
    )


# --------------------------------
# WEBSITE - PRODUCT DETAIL
# --------------------------------

def product_detail(request, cake_id):

    cake = get_object_or_404(
        Cake,
        id=cake_id
    )

    return render(
        request,
        "product-detail.html",
        {
            "cake": cake
        }
    )