from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.permissions import IsProfileOwnerOrReadOnly
from users.serializers import UserSerializer, UserPublicSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]

    def get_serializer_class(self):
        user = self.request.user

        if self.action == 'retrieve':
            instance = self.get_object()
            if instance == user:
                return UserSerializer
            return UserPublicSerializer

        elif self.action == 'list':
            return UserPublicSerializer

        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return UserSerializer




