# Generated by Django 5.0.6 on 2024-06-13 14:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("borrowing", "0004_remove_borrowing_unique_borrowing"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowing",
            name="expected_return_date",
            field=models.DateField(default=datetime.date(2024, 6, 20)),
        ),
    ]
