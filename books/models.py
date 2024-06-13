from django.db import models
from django.db.models import UniqueConstraint


class Book(models.Model):
    COVER_CHOICES = (("hard", "HARD"), ("soft", "SOFT"))
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=255, choices=COVER_CHOICES)
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)
    inventory = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["title"]
        constraints = [UniqueConstraint(fields=["title", "author"], name="unique_book")]
