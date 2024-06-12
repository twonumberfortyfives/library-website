from django.urls import path, include
from rest_framework import routers

from payment import views


router = routers.DefaultRouter()
router.register(r'payment', views.PaymentViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
