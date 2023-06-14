from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('payonline/<int:id>/', views.payment, name='pay_online'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('view_orders/', views.view_orders, name='view_orders'),
]


