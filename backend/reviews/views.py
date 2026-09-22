from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny

from .models import Review
from .serializers import ReviewSerializer

from products.models import Cake
from orders.models import Order, OrderItem

from users.permissions import IsCustomer


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    permission_classes = [IsCustomer]

    # =========================================
    # CUSTOMER'S OWN REVIEWS
    # =========================================

    def get_queryset(self):

        return Review.objects.filter(
            user=self.request.user
        ).select_related(
            "cake",
            "user"
        )

    # =========================================
    # CREATE REVIEW
    # =========================================

    def perform_create(self, serializer):

        cake = serializer.validated_data["cake"]

        # Check whether the logged-in customer
        # has purchased this cake.
        #
        # Cancelled orders are not considered purchases.
        purchased = OrderItem.objects.filter(
            order__user=self.request.user,
            cake=cake
        ).exclude(
            order__status=Order.Status.CANCELLED
        ).exists()

        if not purchased:
            raise ValidationError({
                "detail": "You can review a cake only after purchasing it."
            })

        # Prevent multiple reviews for the same cake
        # by the same customer.
        already_reviewed = Review.objects.filter(
            user=self.request.user,
            cake=cake
        ).exists()

        if already_reviewed:
            raise ValidationError({
                "detail": "You have already reviewed this cake."
            })

        # Save review with the logged-in user.
        serializer.save(
            user=self.request.user
        )

    # =========================================
    # GET REVIEWS FOR A CAKE
    # =========================================

    @action(
        detail=False,
        methods=["get"],
        url_path=r"cake/(?P<cake_id>\d+)",
        permission_classes=[AllowAny]
    )
    def cake_reviews(self, request, cake_id):

        cake = get_object_or_404(
            Cake,
            id=cake_id
        )

        reviews = Review.objects.filter(
            cake=cake
        ).select_related(
            "user"
        ).order_by(
            "-created_at"
        )

        serializer = ReviewSerializer(
            reviews,
            many=True
        )

        return Response(
            serializer.data,
            status=200
        )