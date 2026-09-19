from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

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


        # -------------------------------------
        # CHECK PURCHASE
        # -------------------------------------

        purchased = OrderItem.objects.filter(
            order__user=self.request.user,
            cake=cake
        ).exclude(
            order__status=Order.Status.CANCELLED
        ).exists()


        if not purchased:

            raise ValidationError(
                "You can review a cake only after purchasing it."
            )


        # -------------------------------------
        # PREVENT DUPLICATE REVIEW
        # -------------------------------------

        if Review.objects.filter(
            user=self.request.user,
            cake=cake
        ).exists():

            raise ValidationError(
                "You have already reviewed this cake."
            )


        serializer.save(
            user=self.request.user
        )


    # =========================================
    # GET REVIEWS FOR A CAKE
    # =========================================

    @action(
        detail=False,
        methods=["get"],
        url_path=r"cake/(?P<cake_id>\d+)"
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