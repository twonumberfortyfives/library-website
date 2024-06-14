from decimal import Decimal

import stripe
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView

from borrowing.models import Borrowing
from library_project import settings
from payment.models import Payment
from payment.serializers import PaymentSerializer
from payment.permissions import IsAuthenticatedReadOnlyAdminAll


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session(amount, currency="usd"):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": currency,
                        "product_data": {
                            "name": "Payment for Borrowing",
                        },
                        "unit_amount": int(amount * 100),  # Amount in cents
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=reverse("payment:stripe-success"),
            cancel_url=reverse("payment:stripe-cancel"),
        )
        return session.url, session.id

    except stripe.error.StripeError as e:
        # Handle Stripe errors here
        print(f"Stripe Error: {e}")
        raise  # Re-raise the exception for debugging or logging purposes


class CreatePaymentView(APIView):
    serializer_class = PaymentSerializer

    def post(self, request):
        if self.request.method == "POST":
            borrowing_id = self.request.data.get(
                "borrowing"
            )  # Assuming borrowing is sent as an ID

            # Retrieve the Borrowing object
            borrowing = Borrowing.objects.get(id=borrowing_id)

            if borrowing.actual_return_date:
                period_of_borrowing = (
                    borrowing.actual_return_date - borrowing.borrow_date
                ).days
                borrowing_money = Decimal(period_of_borrowing) * Decimal(
                    borrowing.book.daily_fee
                )
            else:
                borrowing_money = None
            session_url, session_id = create_stripe_session(borrowing_money)

            Payment.objects.create(
                user=request.user,
                borrowing=borrowing,
                session_url=session_url,
                session_id=session_id,
            )
            return redirect(session_url)

        return Response()


class PaymentListView(APIView):
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticatedReadOnlyAdminAll,)

    def get(self, request):
        if self.request.method == "GET":
            if self.request.user.is_authenticated and not self.request.user.is_staff:
                payments = Payment.objects.filter(user=self.request.user)
                serializer = PaymentSerializer(payments, many=True)
                return Response(serializer.data)
            elif self.request.user.is_staff:
                payments = Payment.objects.all()
                serializer = PaymentSerializer(payments, many=True)
                return Response(serializer.data)


class StripeSuccessView(APIView):
    def get(self, request):
        return Response({"message": "Payment successful!"})


class StripeCancelView(APIView):
    def get(self, request):
        return Response({"message": "Payment cancelled."})
