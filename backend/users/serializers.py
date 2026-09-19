from rest_framework import serializers

from .models import User


# =========================================
# REGISTER SERIALIZER
# =========================================

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password",
            "phone",
        ]


    def create(self, validated_data):

        password = validated_data.pop(
            "password"
        )

        user = User(
            **validated_data
        )

        user.set_password(
            password
        )

        user.save()

        return user


# =========================================
# PROFILE SERIALIZER
# =========================================

class ProfileSerializer(serializers.ModelSerializer):

    role = serializers.CharField(
        read_only=True
    )

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "role",
        ]

        read_only_fields = [
            "id",
            "role",
        ]