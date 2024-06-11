from datetime import date, timedelta

from django.db import models
from django.db.models import UniqueConstraint

from books.models import Book
from library_project.settings import AUTH_USER_MODEL


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField(default=date.today() + timedelta(days=7))
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrowings")

    class Meta:
        constraints = [
            UniqueConstraint(fields=['book', 'user'], name='unique_borrowing')
        ]

    def __str__(self):
        return (f"(borrow date: {self.borrow_date}; "
                f"expiration date: {self.actual_return_date}; "
                f"customer: {self.user})")

    @staticmethod
    def validate_borrowing(expected_return_date, raise_error):
        maximum_days_for_borrowing = date.today() + timedelta(days=30)
        if expected_return_date > maximum_days_for_borrowing:
            raise raise_error("Maximum period of borrowing is 30 days")
        elif expected_return_date == date.today():
            raise raise_error("Expected borrowing date is today")
        elif expected_return_date < date.today():
            raise raise_error("Expected borrowing date is in the past")

    def clean(self):
        Borrowing.validate_borrowing(self.expected_return_date, ValueError)

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.clean_fields()
        self.clean()
        return super(Borrowing, self).save(
            force_insert,
            force_update,
            using,
            update_fields
        )
