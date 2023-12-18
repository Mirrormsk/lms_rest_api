from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from lessons.models import Subscription
from lessons.serializers.subscription import SubscriptionSerializer


class SubscriptionCreateAPIView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer


