from django.urls import path

from .views import (
    RegisterView,
    ProfileView,
)


urlpatterns = [

    # REGISTER
    path(
        "register/",
        RegisterView.as_view(),
        name="register"
    ),

    # PROFILE
    path(
        "profile/",
        ProfileView.as_view(),
        name="profile"
    ),

]