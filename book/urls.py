from django.urls import path
from book import views


urlpatterns = [
    path('', views.main_view),
    path('products/', views.ProductListView.as_view()),
    path('products/create/', views.ProductCreateView.as_view()),
    path('products/<int:product_id>/', views.ProductDetailView.as_view()),
    path('products/<int:product_id>/update/', views.ProductUpdateView.as_view()),
    path('category/', views.CategoryListView.as_view()),
    path('category/create/', views.CategoryCreateView.as_view()),
]
