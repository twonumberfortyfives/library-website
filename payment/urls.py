from django.urls import path, include
from rest_framework import routers

from payment.views import (
    CreatePaymentView,
    StripeSuccessView,
    StripeCancelView,
    PaymentListView
)

app_name = 'payment'

router = routers.DefaultRouter()
urlpatterns = [
    path('', include(router.urls)),
    path('create-payment/', CreatePaymentView.as_view(), name='create_payment'),
    path('all-payments/', PaymentListView.as_view(), name='all_payments'),
    path('payments/success/', StripeSuccessView.as_view(), name='stripe-success'),
    path('payments/cancel/', StripeCancelView.as_view(), name='stripe-cancel'),

]
