from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.project_general, name="dash"),
    path('data/customers', views.customers_details, name='customers'),
    path('data/orders', views.order_details, name='orders'),
    path('data/orders_one<int:c_id>', views.get_specific_customer, name='specific'),
    path('data/money<int:c_id>', views.money_details, name='money'),
    path('data/sales<int:p_id>', views.orders_sales, name='sales'),
    path('data/quant<int:p_id>', views.orders_by_month, name='quant'),
]