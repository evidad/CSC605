from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse_lazy
from django.views import generic
from .models import Transaction, Budget
from .serializers import TransactionSerializer, BudgetSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm

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

    context = {
        'transactions': transactions,
        'budgets': budgets,
    }
    return render(request, 'dashboard.html', context)

# Add Transaction View
@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.owner = request.user
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()

    context = {'form': form}
    return render(request, 'add_transaction.html', context)
