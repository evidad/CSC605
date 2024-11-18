from django import forms
from .models import Category, Transaction, Budget

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'description', 'amount', 'transaction_date']
        widgets = {
            'transaction_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(owner=user)


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['month', 'income_goal', 'savings_goal']
