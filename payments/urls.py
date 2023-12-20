from django.urls import path
from payments.apps import PaymentsConfig
from payments.views import PaymentListAPIView, PaymentCreateView, PaymentCheckStatusAPIView

app_name = PaymentsConfig.name

urlpatterns = [
    path('', PaymentListAPIView.as_view(), name='payment-list'),
    path('create/', PaymentCreateView.as_view(), name='payment-create'),
    path('check/', PaymentCheckStatusAPIView.as_view(), name='payment-check'),
]
