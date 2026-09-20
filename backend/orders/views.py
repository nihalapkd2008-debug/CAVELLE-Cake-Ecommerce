from django.db import transaction

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import (
    Cart,
    CartItem,
    Address,
    Order,
    OrderItem,
)

from products.models import Cake

from .serializers import (
    CartSerializer,
    CartItemSerializer,
    AddressSerializer,
    OrderSerializer,
    OrderItemSerializer,
)

from users.permissions import IsCustomer


# =========================================
# CART
# =========================================

class CartViewSet(viewsets.ModelViewSet):

    serializer_class = CartSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):

        return Cart.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


# =========================================
# CART ITEMS
# =========================================

class CartItemViewSet(viewsets.ModelViewSet):

    serializer_class = CartItemSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):

        return CartItem.objects.filter(
            cart__user=self.request.user
        )

    def perform_create(self, serializer):

        cart, created = Cart.objects.get_or_create(
            user=self.request.user
        )

        cake = serializer.validated_data["cake"]
        quantity = serializer.validated_data["quantity"]

        if not cake.is_available:

            raise ValidationError(
                f"{cake.name} is currently unavailable."
            )

        if cake.stock < quantity:

            raise ValidationError(
                f"Only {cake.stock} items available."
            )

        existing_item = CartItem.objects.filter(
            cart=cart,
            cake=cake
        ).first()

        if existing_item:

            new_quantity = (
                existing_item.quantity + quantity
            )

            if new_quantity > cake.stock:

                raise ValidationError(
                    f"Only {cake.stock} items available."
                )

            existing_item.quantity = new_quantity

            existing_item.save()

        else:

            serializer.save(
                cart=cart
            )

    def perform_update(self, serializer):

        cart_item = self.get_object()

        new_quantity = serializer.validated_data.get(
            "quantity",
            cart_item.quantity
        )

        cake = cart_item.cake

        if not cake.is_available:

            raise ValidationError(
                f"{cake.name} is currently unavailable."
            )

        if new_quantity <= 0:

            raise ValidationError(
                "Quantity must be greater than 0."
            )

        if new_quantity > cake.stock:

            raise ValidationError(
                f"Only {cake.stock} items available."
            )

        serializer.save()


# =========================================
# ADDRESS
# =========================================

class AddressViewSet(viewsets.ModelViewSet):

    serializer_class = AddressSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):

        return Address.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


# =========================================
# ORDER
# =========================================

class OrderViewSet(viewsets.ModelViewSet):

    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):

        return Order.objects.filter(
            user=self.request.user
        )

    # =====================================
    # NORMAL CART CHECKOUT
    # =====================================

    @action(
        detail=False,
        methods=["post"]
    )
    @transaction.atomic
    def checkout(self, request):

        cart = Cart.objects.filter(
            user=request.user
        ).first()

        if not cart:

            raise ValidationError(
                "Cart not found."
            )

        cart_items = CartItem.objects.filter(
            cart=cart
        ).select_related("cake")

        if not cart_items.exists():

            raise ValidationError(
                "Cart is empty."
            )

        address_id = request.data.get(
            "address"
        )

        if not address_id:

            raise ValidationError(
                "Address is required."
            )

        address = Address.objects.filter(
            id=address_id,
            user=request.user
        ).first()

        if not address:

            raise ValidationError(
                "Invalid address."
            )

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

            total += (
                cake.price *
                cart_item.quantity
            )

        order.total_amount = total

        order.save(
            update_fields=["total_amount"]
        )

        cart_items.delete()

        return Response(
            OrderSerializer(order).data,
            status=201
        )

    # =====================================
    # BUY NOW CHECKOUT
    # =====================================

    @action(
        detail=False,
        methods=["post"],
        url_path="buy-now-checkout"
    )
    @transaction.atomic
    def buy_now_checkout(self, request):

        cake_id = request.data.get(
            "cake"
        )

        quantity = request.data.get(
            "quantity"
        )

        address_id = request.data.get(
            "address"
        )

        # ---------------------------------
        # CAKE CHECK
        # ---------------------------------

        if not cake_id:

            raise ValidationError(
                "Cake is required."
            )

        # ---------------------------------
        # ADDRESS CHECK
        # ---------------------------------

        if not address_id:

            raise ValidationError(
                "Address is required."
            )

        # ---------------------------------
        # QUANTITY CHECK
        # ---------------------------------

        try:

            quantity = int(
                quantity
            )

        except (
            TypeError,
            ValueError
        ):

            raise ValidationError(
                "Quantity must be a valid number."
            )

        if quantity <= 0:

            raise ValidationError(
                "Quantity must be greater than 0."
            )

        # ---------------------------------
        # GET CAKE
        # ---------------------------------

        cake = Cake.objects.filter(
            id=cake_id
        ).first()

        if not cake:

            raise ValidationError(
                "Cake not found."
            )

        # ---------------------------------
        # GET USER ADDRESS
        # ---------------------------------

        address = Address.objects.filter(
            id=address_id,
            user=request.user
        ).first()

        if not address:

            raise ValidationError(
                "Invalid address."
            )

        # ---------------------------------
        # AVAILABILITY CHECK
        # ---------------------------------

        if not cake.is_available:

            raise ValidationError(
                f"{cake.name} is currently unavailable."
            )

        # ---------------------------------
        # STOCK CHECK
        # ---------------------------------

        if cake.stock < quantity:

            raise ValidationError(
                f"Only {cake.stock} item(s) are available for {cake.name}."
            )

        # ---------------------------------
        # TOTAL AMOUNT
        # ---------------------------------

        total_amount = (
            cake.price *
            quantity
        )

        # ---------------------------------
        # CREATE ORDER
        # ---------------------------------

        order = Order.objects.create(
            user=request.user,
            address=address,
            status="pending",
            total_amount=total_amount
        )

        # ---------------------------------
        # CREATE ORDER ITEM
        # ---------------------------------

        OrderItem.objects.create(
            order=order,
            cake=cake,
            quantity=quantity,
            unit_price=cake.price
        )

        # ---------------------------------
        # REDUCE STOCK
        # ---------------------------------

        cake.stock -= quantity

        cake.save(
            update_fields=["stock"]
        )

        # ---------------------------------
        # RETURN ORDER
        # ---------------------------------

        return Response(
            OrderSerializer(order).data,
            status=201
        )


# =========================================
# ORDER ITEMS
# =========================================

class OrderItemViewSet(viewsets.ModelViewSet):

    serializer_class = OrderItemSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):

        return OrderItem.objects.filter(
            order__user=self.request.user
        )


# =========================================
# STAFF ORDER MANAGEMENT
# =========================================

class StaffOrderViewSet(viewsets.ModelViewSet):

    serializer_class = OrderSerializer

    def get_queryset(self):

        return Order.objects.select_related(
            "user",
            "address"
        ).prefetch_related(
            "items"
        ).all()

    def get_permissions(self):

        from users.permissions import IsStaffOrAdmin

        return [
            IsStaffOrAdmin()
        ]

    def perform_update(self, serializer):

        order = self.get_object()

        new_status = serializer.validated_data.get(
            "status",
            order.status
        )

        allowed_statuses = [
            Order.Status.PENDING,
            Order.Status.CONFIRMED,
            Order.Status.PREPARING,
            Order.Status.READY,
            Order.Status.DELIVERED,
            Order.Status.CANCELLED,
        ]

        if new_status not in allowed_statuses:

            raise ValidationError(
                "Invalid order status."
            )

        serializer.save()