# Generated by Django 5.0.6 on 2024-06-12 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0003_remove_book_inventory"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="inventory",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
