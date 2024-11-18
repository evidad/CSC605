from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model

class Category(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
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

    @property
    def total_expenses(self):
        return (
            Transaction.objects.filter(owner=self.owner, transaction_date__month=self.created_on.month)
            .aggregate(total=Sum('amount'))['total']
            or 0.00
        )

    @property
    def remaining_budget(self):
        return self.income_goal - self.total_expenses
    
    def __str__(self):
        return f"{self.owner}'s Budget for {self.month}"