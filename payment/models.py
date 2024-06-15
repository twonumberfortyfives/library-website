from decimal import Decimal

from django.db import models

from borrowing.models import Borrowing
from customers.models import User


class Payment(models.Model):
    CHOICES_STATUS = (
        ("pending", "PENDING"),
        ("paid", "PAID"),
    )
    CHOICES_TYPE = (("payment", "PAYMENT"), ("fine", "FINE"))
    status = models.CharField(choices=CHOICES_STATUS, max_length=10, default="pending")
    type = models.CharField(choices=CHOICES_TYPE, max_length=10, default="payment")
    borrowing = models.ForeignKey(
        Borrowing, on_delete=models.CASCADE, related_name="payments"
    )
    session_url = models.CharField(max_length=10000)
    session_id = models.CharField(max_length=10000)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payments", default=None, null=True
    )

    @property
    def money_to_pay(self):
        if self.borrowing.actual_return_date:
            period_of_borrowing = (
                self.borrowing.actual_return_date - self.borrowing.borrow_date
            ).days
            borrowing_money = Decimal(period_of_borrowing) * Decimal(
                self.borrowing.book.daily_fee
            )
            return borrowing_money
        else:
            return None
