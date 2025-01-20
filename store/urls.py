from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.store_list, name='store_list'),
    path('store/categories/<slug:category_slug>/', views.store_list, name='category_products'),
    path('store/products/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('store/', views.store_search, name='store_search'),
]