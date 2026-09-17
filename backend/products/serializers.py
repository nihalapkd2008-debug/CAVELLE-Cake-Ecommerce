from rest_framework import serializers
from .models import Category, Cake


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CakeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cake
        fields = "__all__"

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0."
            )
        return value

    def validate_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Weight must be greater than 0."
            )
        return value