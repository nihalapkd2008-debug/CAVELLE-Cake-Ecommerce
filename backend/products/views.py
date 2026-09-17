from rest_framework import viewsets

from .models import Category, Cake
from .serializers import CategorySerializer, CakeSerializer
from users.permissions import IsStaffOrAdmin


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrAdmin]


class CakeViewSet(viewsets.ModelViewSet):
    queryset = Cake.objects.select_related(
        "category"
    ).prefetch_related(
        "reviews"
    )
    serializer_class = CakeSerializer
    permission_classes = [IsStaffOrAdmin]