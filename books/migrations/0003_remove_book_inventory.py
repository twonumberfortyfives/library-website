# Generated by Django 5.0.6 on 2024-06-12 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0002_alter_book_options_book_unique_book"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="inventory",
        ),
    ]
