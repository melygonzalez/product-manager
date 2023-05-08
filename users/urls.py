from django.urls import path
from products import views
from users.views import user_list, user_approval

urlpatterns = [
    path('', user_list),
    path('<int:pk>/', views.product_detail),
    path('<int:pk>/approve', user_approval),
]