from django.urls import path
from products.views import product_list, product_detail

urlpatterns = [
    path('', product_list),
    path('<int:pk>/', product_detail),
]
