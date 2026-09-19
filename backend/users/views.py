from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    RegisterSerializer,
    ProfileSerializer,
)


# =========================================
# REGISTER
# =========================================

class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer


# =========================================
# PROFILE
# =========================================

class ProfileView(
    generics.RetrieveUpdateAPIView
):

    serializer_class = ProfileSerializer

    permission_classes = [
        IsAuthenticated
    ]


    def get_object(self):

        return self.request.user