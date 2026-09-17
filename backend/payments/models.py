from django.db import models
from orders.models import Order


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESSFUL = "successful", "Successful"
        FAILED = "failed", "Failed"

    class Method(models.TextChoices):
        COD = "cod", "Cash on Delivery"
        CARD = "card", "Card"
        UPI = "upi", "UPI"

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=20,
        choices=Method.choices
    )
    payment_status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    transaction_id = models.CharField(
        max_length=100,
        blank=True
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)