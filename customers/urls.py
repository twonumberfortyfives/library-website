from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import CreateUserView, ManageUserView, VerifyEmail, SignUp

app_name = 'customers'

urlpatterns = [
    path('register/', SignUp.as_view(), name='register'),
    path('me/', ManageUserView.as_view(), name='manage-user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
]
