import datetime

from rest_framework import serializers

from borrowing.models import Borrowing


class BorrowingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = '__all__'


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "expected_return_date", "book")

    def validate(self, attrs):
        Borrowing.validate_borrowing(
            expected_return_date=attrs["expected_return_date"],
            raise_error=serializers.ValidationError,
            )
        return attrs
