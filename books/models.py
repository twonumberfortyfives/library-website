from django.db import models


class Book(models.Model):
    COVER_CHOICES = (
        ("hard", "HARD"),
        ("soft", "SOFT")
    )
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=255, choices=COVER_CHOICES)
    inventory = models.IntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)