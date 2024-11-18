from django.contrib import admin
from django.urls import path, include
from kakeibo_finance.views import CustomLoginView, SignupView, dashboard, add_transaction, edit_transaction, delete_transaction, add_budget, edit_budget, category_list, add_category, edit_category, delete_category
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.shortcuts import redirect  # Import redirect

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('', lambda request: redirect('login'), name='home'),  # Redirect root URL to login
    path('dashboard/', dashboard, name='dashboard'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('add-transaction/', add_transaction, name='add_transaction'),
    path('transaction/edit/<int:transaction_id>/', edit_transaction, name='edit_transaction'),
    path('transaction/delete/<int:transaction_id>/', delete_transaction, name='delete_transaction'),
    path('add-budget/', add_budget, name='add_budget'),
    path('edit-budget/<int:budget_id>/', edit_budget, name='edit_budget'),
    path('categories/', category_list, name='category_list'),
    path('categories/add/', add_category, name='add_category'),
    path('categories/edit/<int:category_id>/', edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', delete_category, name='delete_category'),
    
    path('admin/', admin.site.urls),
    path('api/v1/kakeibo/', include('kakeibo_finance.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
