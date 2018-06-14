from django.urls import path
from . import views


app_name = 'shop'
urlpatterns = [
    path('', views.ProductsView.as_view(), name='product_list'),
    path('<str:category_slug>/', views.ProductsView.as_view(), name='product_list_by_category'),
    path('<int:id>/<str:slug>/', views.ProductView.as_view(), name='product_detail'),
]