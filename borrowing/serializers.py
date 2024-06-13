from rest_framework import serializers

from books.models import Book
from borrowing.models import Borrowing


class BookForBorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "daily_fee")


class BorrowingListSerializer(serializers.ModelSerializer):
    book = BookForBorrowingSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        )


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "expected_return_date",
            "book",
        )

    def validate(self, attrs):
        expected_return_date = attrs.get("expected_return_date")
        if expected_return_date:
            Borrowing.validate_borrowing(
                expected_return_date=expected_return_date,
                raise_error=serializers.ValidationError,
            )
        return attrs

    def create(self, validated_data):
        if int(validated_data.get("book").inventory) <= 0:
            raise serializers.ValidationError("Inventory is empty")
        print(validated_data.get("book").inventory)
        borrowing = Borrowing.objects.create(**validated_data)
        return borrowing
