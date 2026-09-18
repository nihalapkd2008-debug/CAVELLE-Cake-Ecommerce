from rest_framework import serializers

from .models import (
    Cart,
    CartItem,
    Address,
    Order,
    OrderItem,
)


class CartItemSerializer(serializers.ModelSerializer):

    cart = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    cake_name = serializers.CharField(
        source="cake.name",
        read_only=True
    )

    cake_price = serializers.DecimalField(
        source="cake.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    cake_image = serializers.ImageField(
        source="cake.image",
        read_only=True
    )

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "cart",
            "cake",
            "cake_name",
            "cake_price",
            "cake_image",
            "quantity",
            "subtotal",
        ]

    def validate_quantity(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than 0."
            )

        return value

    def get_subtotal(self, obj):

        return obj.cake.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    items = CartItemSerializer(
        source="items",
        many=True,
        read_only=True
    )

    class Meta:
        model = Cart
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

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

    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    items = OrderItemSerializer(
        source="items",
        many=True,
        read_only=True
    )

    class Meta:
        model = Order
        fields = "__all__"