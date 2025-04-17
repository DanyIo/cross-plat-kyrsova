from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "amount",
            "category",
            "transaction_type",
            "date",
            "description",
            "user",
        ]
        read_only_fields = ["user"]
