from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_all_prints, name='show_all_prints'),
    path('add_product/', views.add_product, name='add_product'),
    path('<product_name>/', views.product_details, name='product_details'),
]
