from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse_lazy
from django.views import generic
from .models import Category, Transaction, Budget
from .serializers import TransactionSerializer, BudgetSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, TransactionForm, BudgetForm

# Transaction Views
class TransactionListView(ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

class TransactionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsOwnerOrReadOnly]

# Budget Views
class BudgetListView(ListCreateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

class BudgetDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsOwnerOrReadOnly]

# Login View
class CustomLoginView(LoginView):
    template_name = 'login.html'

# Signup View
class SignupView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Redirect to login after successful signup
    template_name = 'signup.html'

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    user = request.user
    transactions = Transaction.objects.filter(owner=user).order_by('-transaction_date')
    budgets = Budget.objects.filter(owner=user).order_by('-created_on')
    categories = Category.objects.filter(owner=user).order_by('name')

    # # Add budget tracking calculations
    # for budget in budgets:
    #     budget.total_expenses = budget.total_expenses  # Automatically calculated
    #     budget.remaining_budget = budget.remaining_budget
    
    context = {
        'transactions': transactions,
        'categories': categories,
        'budgets': [
            {
                'month': budget.month,
                'income_goal': budget.income_goal,
                'total_expenses': round(budget.total_expenses, 2),
                'remaining_budget': round(budget.remaining_budget, 2),
            }
            for budget in budgets
        ],
    }
    return render(request, 'dashboard.html', context)

# Add Transaction View
@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.owner = request.user
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm(user=request.user)

    context = {'form': form}
    return render(request, 'add_transaction.html', context)

# Edit Transaction View
@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, owner=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TransactionForm(instance=transaction, user=request.user)
    return render(request, 'edit_transaction.html', {'form': form})

# Delete Transaction View
@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, owner=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('dashboard')
    return render(request, 'delete_transaction.html', {'transaction': transaction})

@login_required
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.owner = request.user
            budget.save()
            return redirect('dashboard')
    else:
        form = BudgetForm()
    return render(request, 'add_budget.html', {'form': form})

# Budget View
@login_required
def edit_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, owner=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'edit_budget.html', {'form': form})

# Category View
@login_required
def category_list(request):
    categories = Category.objects.filter(owner=request.user)
    return render(request, 'category_list.html', {'categories': categories})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.owner = request.user
            category.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, owner=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, owner=request.user)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'delete_category.html', {'category': category})