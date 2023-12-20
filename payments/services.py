import environ
import stripe
from rest_framework import status
from rest_framework.response import Response
from stripe import Product, Price
from stripe.checkout import Session

from payments.models import Payment
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
        match payment.method:

            case Payment.METHOD_CASH:
                return Response(
                    {"status": "success"},
                    status=status.HTTP_201_CREATED,
                )

            case Payment.METHOD_TRANSFER_TO_ACCOUNT:
                payment_session = StripeApiClient.execute_payment(payment)
                payment_data = PaymentSerializer(payment)
                return Response(
                    {
                        "status": "success",
                        "payment_session_id": payment_session.id,
                        "checkout_url": payment_session.url,
                        "payment": payment_data.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
