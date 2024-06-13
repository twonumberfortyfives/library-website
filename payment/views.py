from decimal import Decimal

import requests
import stripe
from django.db import transaction
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from borrowing.models import Borrowing
from library_project import settings
from payment.models import Payment
from payment.serializers import PaymentSerializer


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session(amount, currency='usd'):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': 'Payment for Borrowing',
                    },
                    'unit_amount': int(amount * 100),  # Amount in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8000/api/library-payments/payments/success/',
            cancel_url='http://localhost:8000/api/library-payments/payments/cancel/',
        )
        return session.url, session.id

    except stripe.error.StripeError as e:
        # Handle Stripe errors here
        print(f"Stripe Error: {e}")
        raise  # Re-raise the exception for debugging or logging purposes


def check_and_update_payment_status():
    try:
        all_payments = Payment.objects.all()

        session_ids = [payment.session_id for payment in all_payments]

        checkout_sessions = stripe.checkout.Session.list(
            limit=len(session_ids),
            ids=session_ids
        )

        # creating dict to accelerate finding session_id
        session_status_map = {session.id: session.payment_status for session in checkout_sessions}

        with transaction.atomic():
            for payment in all_payments:
                payment_status = session_status_map.get(payment.session_id)
                if payment_status == 'paid' and payment.status != 'paid':
                    payment.status = 'paid'
                    payment.save()

    except stripe.error.StripeError as e:
        print(f"Stripe Error: {e}")
        return False

    return True


class CreatePaymentView(APIView):
    serializer_class = PaymentSerializer

    def post(self, request):
        if self.request.method == 'POST':
            borrowing_id = self.request.data.get("borrowing")  # Assuming borrowing is sent as an ID

            # Retrieve the Borrowing object
            borrowing = Borrowing.objects.get(id=borrowing_id)

            if borrowing.actual_return_date:
                period_of_borrowing = (borrowing.actual_return_date - borrowing.borrow_date).days
                borrowing_money = Decimal(period_of_borrowing) * Decimal(borrowing.book.daily_fee)
            else:
                borrowing_money = None
            print(borrowing_money)
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

    def get(self, request):
        if self.request.method == 'GET':
            if self.request.user.is_authenticated and not self.request.user.is_staff:
                payments = Payment.objects.filter(user=self.request.user)
                serializer = PaymentSerializer(payments, many=True)
                return Response(serializer.data)
            elif self.request.user.is_staff:
                payments = Payment.objects.all()
                serializer = PaymentSerializer(payments, many=True)
                return Response(serializer.data)
            return Response(status=status.HTTP_404_NOT_FOUND)


class StripeSuccessView(APIView):
    def get(self, request):
        return Response({'message': 'Payment successful!'})


class StripeCancelView(APIView):
    def get(self, request):
        return Response({'message': 'Payment cancelled.'})
