from rest_framework import serializers
from .models import Cart, CartItem
from .models import Address
from .models import Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = "__all__"

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than 0."
            )
        return value


class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    items = CartItemSerializer(
        source="cartitem_set",
        many=True,
        read_only=True
    )

    class Meta:
        model = Cart
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Address
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = "__all__"

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than 0."
            )
        return value


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    items = OrderItemSerializer(
        source="items",
        many=True,
        read_only=True
    )

    class Meta:
        model = Order
        fields = "__all__"