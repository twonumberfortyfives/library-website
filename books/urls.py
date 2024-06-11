from rest_framework import routers

from books.views import BookViewSet

router = routers.DefaultRouter()

router.register(r'books', BookViewSet)

app_name = 'books'

urlpatterns = []
