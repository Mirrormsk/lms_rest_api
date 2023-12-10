from rest_framework import serializers

from users.models import User
from payments.serializers import PaymentSerializer


class UserSerializer(serializers.ModelSerializer):

    payments = PaymentSerializer(many=True, read_only=True, source='payment_set')

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id']
