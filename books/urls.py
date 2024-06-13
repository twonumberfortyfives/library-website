from rest_framework import routers

from books.views import BookViewSet

router = routers.DefaultRouter()

router.register("books", BookViewSet)

app_name = "books"

urlpatterns = router.urls
