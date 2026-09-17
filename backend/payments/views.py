from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Payment
from .serializers import PaymentSerializer
from orders.models import Order
from users.permissions import IsCustomer


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return Payment.objects.filter(
            order__user=self.request.user
        )

    @action(detail=False, methods=["post"])
    def create_payment(self, request):
        order_id = request.data.get("order")
        method = request.data.get("payment_method")

        if not order_id:
            raise ValidationError("Order is required.")

        if not method:
            raise ValidationError("Payment method is required.")

        order = Order.objects.filter(
            id=order_id,
            user=request.user
        ).first()

        if not order:
            raise ValidationError("Invalid order.")

        if Payment.objects.filter(order=order).exists():
            raise ValidationError(
                "Payment already exists for this order."
            )

        payment = Payment.objects.create(
            order=order,
            amount=order.total_amount,
            payment_method=method,
            payment_status=Payment.Status.PENDING
        )

        return Response(
            PaymentSerializer(payment).data,
            status=201
        )