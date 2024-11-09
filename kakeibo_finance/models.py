from django.db import models
from django.contrib.auth import get_user_model

class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ('INCOME', 'Income'),
        ('ESSENTIAL', 'Essential'),
        ('WANTS', 'Wants'),
        ('SAVINGS', 'Savings'),
        ('OTHER', 'Other')
    ]
    
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=256)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category}: {self.amount}"

class Budget(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    income_goal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    savings_goal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner}'s Budget for {self.month}"