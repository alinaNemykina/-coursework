from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='list'),
    path('prod/<int:pk>/', views.prod_detail, name='prod_detail'),
    path('client/au/', views.create_client, name='create_client'),
    path('order/', views.order_new, name='order_new'),
    path('my_orders/', views.get_orders, name='orders'),
    path('add_product/', views.add_product, name='add_product'),
    path('login/', views.authent, name='authent'),
]