import stripe
from celery import shared_task

from payment.models import Payment


@shared_task
def check_payment_status():
    list_of_result = []
    try:
        all_payments = Payment.objects.all()
        for payment in all_payments:
            checkout_session = stripe.checkout.Session.retrieve(payment.session_id)
            payment_status = checkout_session.payment_status
            list_of_result.append(payment_status)
            if checkout_session.payment_status == 'paid':
                payment.status = 'paid'
                payment.save()
    except stripe.error.StripeError as e:
        print(f"Stripe Error: {e}")
