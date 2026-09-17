from rest_framework import viewsets

from .models import Review
from .serializers import ReviewSerializer
from users.permissions import IsCustomer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return Review.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )