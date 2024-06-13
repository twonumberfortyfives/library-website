# Generated by Django 5.0.6 on 2024-06-11 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="book",
            options={"ordering": ["title"]},
        ),
        migrations.AddConstraint(
            model_name="book",
            constraint=models.UniqueConstraint(
                fields=("title", "author"), name="unique_book"
            ),
        ),
    ]