from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Cart, CartItem, Address, Order, OrderItem
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    AddressSerializer,
    OrderSerializer,
    OrderItemSerializer,
)

from users.permissions import IsCustomer


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return Cart.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return CartItem.objects.filter(
            cart__user=self.request.user
        )


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return Address.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        )

    @action(detail=False, methods=["post"])
    @transaction.atomic
    def checkout(self, request):
        cart = Cart.objects.filter(
            user=request.user
        ).first()

        if not cart:
            raise ValidationError("Cart not found.")

        cart_items = CartItem.objects.filter(
            cart=cart
        ).select_related("cake")

        if not cart_items.exists():
            raise ValidationError("Cart is empty.")

        address_id = request.data.get("address")

        if not address_id:
            raise ValidationError("Address is required.")

        address = Address.objects.filter(
            id=address_id,
            user=request.user
        ).first()

        if not address:
            raise ValidationError("Invalid address.")

        order = Order.objects.create(
            user=request.user,
            address=address,
            total_amount=0
        )

        total = 0

        for cart_item in cart_items:
            cake = cart_item.cake

            if not cake.is_available:
                raise ValidationError(
                    f"{cake.name} is currently unavailable."
                )

            if cake.stock < cart_item.quantity:
                raise ValidationError(
                    f"Insufficient stock for {cake.name}."
                )

            OrderItem.objects.create(
                order=order,
                cake=cake,
                quantity=cart_item.quantity,
                unit_price=cake.price
            )

            cake.stock -= cart_item.quantity
            cake.save(
                update_fields=["stock"]
            )

            total += cake.price * cart_item.quantity

        order.total_amount = total
        order.save(
            update_fields=["total_amount"]
        )

        cart_items.delete()

        return Response(
            OrderSerializer(order).data,
            status=201
        )


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return OrderItem.objects.filter(
            order__user=self.request.user
        )