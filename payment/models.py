from django.db import models

from borrowing.models import Borrowing


class Payment(models.Model):
    CHOICES_STATUS = (
        ("pending", "PENDING"),
        ("paid", "PAID"),
    )
    CHOICES_TYPE = (
        ("payment", "PAYMENT"),
        ("fine", "FINE")
    )
    status = models.CharField(choices=CHOICES_STATUS, max_length=10, default="pending")
    type = models.CharField(choices=CHOICES_TYPE, max_length=10, default="payment")
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE, related_name="payments")
    session_url = models.URLField(max_length=10000)
    session_id = models.CharField(max_length=10000)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
