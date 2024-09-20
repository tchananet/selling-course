from rest_framework.serializers import Serializer, ModelSerializer
from .models import CourseSales, Transaction

class SalesSerializer(Serializer):
    class Meta:
        model = CourseSales
        fields = "__all__"

class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"