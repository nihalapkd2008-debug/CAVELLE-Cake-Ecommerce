from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Category, Cake
from .serializers import CategorySerializer, CakeSerializer

from users.permissions import IsStaffOrAdmin


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

    permission_classes = [IsStaffOrAdminOrReadOnly]


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

    permission_classes = [IsStaffOrAdminOrReadOnly]


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
        {"cakes": cakes}
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
        {"cake": cake}
    )