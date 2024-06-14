from rest_framework import serializers

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    money_to_pay = serializers.IntegerField(read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"
