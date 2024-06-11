from rest_framework import routers

from borrowing.views import BorrowViewSet

router = routers.DefaultRouter()

router.register('borrowings', BorrowViewSet)

app_name = 'borrowing'

urlpatterns = router.urls

