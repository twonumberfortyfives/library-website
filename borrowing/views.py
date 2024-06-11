from rest_framework import viewsets

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer, BorrowingListSerializer
from borrowing.permissions import IsAuthenticatedEmailVerifiedReadOnlyAdminAll


class BorrowViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowingSerializer
    queryset = Borrowing.objects.all()
    permission_classes = (IsAuthenticatedEmailVerifiedReadOnlyAdminAll,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return BorrowingListSerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
