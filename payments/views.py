from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from payments.models import Payment
from payments.serializers import (
    PaymentSerializer,
    PaymentCreateSerializer,
    PaymentCheckStatusSerializer,
)
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

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user": openapi.Schema(type=openapi.TYPE_INTEGER, description="User ID"),
                "lesson": openapi.Schema(type=openapi.TYPE_INTEGER, description="Lesson ID"),
                "course": openapi.Schema(type=openapi.TYPE_INTEGER, description="Course ID"),
                "method": openapi.Schema(type=openapi.TYPE_STRING, enum=["cash", "account"], description="Payment method"),
                "amount": openapi.Schema(type=openapi.TYPE_INTEGER, description="Amount"),
            },
            required=["user",  "method", "amount"],

            )
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()
            response = PaymentService.process_payment(payment)
            return response
        else:
            return Response(
                {"status": "failed", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PaymentCheckStatusAPIView(APIView):
    """
    Check payment status (by id).
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentCheckStatusSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'payment_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Payment id')
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(description="Payment info", schema=PaymentSerializer)
        }
    )
    def post(self, request, *args, **kwargs):
        payment_id = request.data.get("payment_id")
        try:
            payment = Payment.objects.get(pk=payment_id)
        except Payment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return PaymentService.update_payment_status(payment)
