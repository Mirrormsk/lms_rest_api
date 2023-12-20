from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from payments.models import Payment
from payments.serializers import PaymentSerializer, PaymentCreateSerializer
from payments.services import StripeApiClient, PaymentService


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["course", "lesson", "method"]
    search_fields = ["course", "lesson__title", "method"]
    ordering_fields = ["created_at"]


class PaymentCreateView(APIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()
            response = PaymentService.process_payment(payment)
            return response
        else:
            return Response({"status": "failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


