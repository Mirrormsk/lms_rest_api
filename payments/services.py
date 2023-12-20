from typing import Literal

import environ
import stripe
from rest_framework import status
from rest_framework.response import Response
from stripe import Product, Price
from stripe.checkout import Session

from payments.models import Payment, PaymentSession
from payments.serializers import PaymentSerializer

env = environ.Env(DEBUG=(bool, False))

stripe.api_key = env("STRIPE_API_KEY")
SUCCESS_URL = env("PAYMENT_SUCCESS_URL")
DEFAULT_PAYMENT_QUANTITY = env("DEFAULT_PAYMENT_QUANTITY")


class StripeApiClient:
    """Stripe API Client class"""

    @staticmethod
    def create_product(name: str, description: str) -> Product:
        product = stripe.Product.create(name=name, description=description)
        return product

    @staticmethod
    def create_price(amount: int, currency: str, product_id: str) -> Price:
        price = stripe.Price.create(
            unit_amount=amount,
            currency=currency,
            product=product_id,
        )
        return price

    @staticmethod
    def create_session(price: Price, quantity: int) -> Session:
        session = stripe.checkout.Session.create(
            success_url=SUCCESS_URL,
            line_items=[{"price": price.id, "quantity": quantity}],
            mode="payment",
        )
        return session

    @classmethod
    def execute_payment(
        cls, payment: Payment, quantity: int = DEFAULT_PAYMENT_QUANTITY
    ) -> Session:
        product = payment.course if payment.course else payment.lesson
        stripe_product = cls.create_product(
            name=product.title, description=product.description
        )
        stripe_price = cls.create_price(
            amount=payment.amount, currency="USD", product_id=stripe_product.id
        )
        session = cls.create_session(price=stripe_price, quantity=quantity)
        return session

    @staticmethod
    def retrieve_session(session_id: str) -> Session:
        session = stripe.checkout.Session.retrieve(session_id)
        return session


class PaymentService:
    """Payment service"""

    @staticmethod
    def process_payment(payment: Payment) -> Response:
        """Processing payment"""
        payment_data = PaymentSerializer(payment)

        match payment.method:

            case Payment.METHOD_CASH:
                payment.is_paid = True
                payment.save()

                return Response(
                    {
                        "status": "success",
                        "payment_session_id": None,
                        "checkout_url": None,
                        "payment": payment_data.data,
                    },
                    status=status.HTTP_201_CREATED,
                )

            case Payment.METHOD_TRANSFER_TO_ACCOUNT:
                payment_session = StripeApiClient.execute_payment(payment)

                session_obj = PaymentSession.objects.create(
                    payment=payment, session_id=payment_session.id
                )
                session_obj.save()

                return Response(
                    {
                        "status": "success",
                        "payment_session_id": payment_session.id,
                        "checkout_url": payment_session.url,
                        "payment": payment_data.data,
                    },
                    status=status.HTTP_201_CREATED,
                )

    @staticmethod
    def get_payment_status(
        payment: Payment,
    ) -> Literal["complete", "expired", "open"] | None:
        session_id = payment.session.session_id
        session = StripeApiClient.retrieve_session(session_id)
        session_status = session.status
        return session_status

    @classmethod
    def update_payment_status(cls, payment: Payment) -> Response:
        payment_data = PaymentSerializer(payment).data

        if payment.is_paid or payment.method == Payment.METHOD_CASH:
            return Response(payment_data, status=status.HTTP_200_OK)

        try:
            payment_session_status = cls.get_payment_status(payment)
        except Payment.session.RelatedObjectDoesNotExist:
            return Response(
                {"status": "failed", "message": "Can't find session for this payment"},
                status=status.HTTP_206_PARTIAL_CONTENT,
            )
        else:
            if payment_session_status == "complete":
                payment.is_paid = True
                payment.save()
                payment_data = PaymentSerializer(payment).data
                return Response(payment_data, status=status.HTTP_200_OK)
