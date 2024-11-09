from rest_framework import serializers
from .models import Transaction
from .models import Budget

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "id",
            "owner",
            "category",
            "description",
            "amount",
            "transaction_date",
            "created_on",
            "updated_on",
        )

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = (
            "id",
            "owner",
            "month",
            "income_goal",
            "savings_goal",
            "created_on",
            "updated_on",
        )