from rest_framework import serializers
from payments.models import Payment
from users.models import User


class PaymentSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField("email", queryset=User.objects.all())
    method = serializers.CharField(source='get_method_display')

    class Meta:
        model = Payment
        fields = "__all__"

