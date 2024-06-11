from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Book.objects.all(),
                fields=['title', 'author']
            )
        ]
