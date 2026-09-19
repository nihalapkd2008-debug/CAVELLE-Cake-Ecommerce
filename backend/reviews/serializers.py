from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "username",
            "cake",
            "rating",
            "comment",
            "created_at",
            "updated_at",
        ]

    def validate_rating(self, value):

        if value < 1 or value > 5:

            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )

        return value