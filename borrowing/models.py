from datetime import date, timedelta

from django.db import models

from books.models import Book
from library_project.settings import AUTH_USER_MODEL


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField(default=date.today() + timedelta(days=7))
    actual_return_date = models.DateField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrowings")

    def __str__(self):
        return (f"(borrow date: {self.borrow_date}; "
                f"expiration date: {self.actual_return_date}; "
                f"customer: {self.user})")
