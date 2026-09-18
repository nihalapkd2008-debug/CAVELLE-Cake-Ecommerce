from rest_framework import viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Category, Cake
from .serializers import CategorySerializer, CakeSerializer


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


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrAdminOrReadOnly]


class CakeViewSet(viewsets.ModelViewSet):
    queryset = Cake.objects.select_related(
        "category"
    ).prefetch_related(
        "reviews"
    )
    serializer_class = CakeSerializer
    permission_classes = [IsStaffOrAdminOrReadOnly]