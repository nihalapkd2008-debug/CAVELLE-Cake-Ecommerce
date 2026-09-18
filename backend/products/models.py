from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    description = models.TextField(blank=True)

    image = models.ImageField(
        upload_to="categories/",
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Cake(models.Model):
    name = models.CharField(max_length=150)

    description = models.TextField()

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="cakes"
    )

    wishlist_users = models.ManyToManyField(
        "users.User",
        blank=True,
        related_name="wishlist_cakes"
    )

    flavour = models.CharField(max_length=100)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to="cakes/",
        blank=True
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    is_available = models.BooleanField(
        default=True
    )

    eggless = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

class BakeryItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="cakes/")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name