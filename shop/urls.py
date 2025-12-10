from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views


urlpatterns = [
    # API Root
    path('', views.APIRootView.as_view(), name='api-root'),
    
    # Auth
    path('auth/register', views.RegisterView.as_view()),
    path('auth/login', views.LoginView.as_view()),
    path('auth/refresh', TokenRefreshView.as_view()),
    path('auth/me', views.MeView.as_view()),

    # Products
    path('products/', views.ProductListView.as_view()),
    path('products/<slug:slug>/', views.ProductDetailView.as_view()),
    path('products/id/<int:pk>/', views.ProductDetailByIdView.as_view()),  # Support ID lookup
    path('products/add', views.ProductCreateView.as_view()),
    path('products/<int:pk>/edit', views.ProductUpdateView.as_view()),
    path('products/<int:pk>/delete', views.ProductDeleteView.as_view()),

    # Categories
    path('categories/', views.CategoryListView.as_view()),
    path('categories/add', views.CategoryCreateView.as_view()),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view()),

    # Banners
    path('banners/', views.BannerListView.as_view()),
    path('banners/upload', views.BannerUploadView.as_view()),
    path('banners/<int:pk>/', views.BannerDeleteView.as_view()),

    # Cart
    path('cart/', views.CartView.as_view()),
    path('cart/add', views.CartAddView.as_view()),
    path('cart/update', views.CartUpdateView.as_view()),
    path('cart/remove/<int:pk>', views.CartRemoveView.as_view()),

    # Orders
    path('orders/checkout', views.CheckoutView.as_view()),
    path('orders/confirm-payment', views.ConfirmPaymentView.as_view()),
    path('orders/my-orders', views.MyOrdersView.as_view()),

    # Admin orders
    path('orders/', views.AdminOrdersView.as_view()),
    path('orders/<int:pk>/', views.AdminOrderDetailView.as_view()),
    path('orders/<int:pk>/mark-paid', views.AdminMarkPaidView.as_view()),
    path('orders/<int:pk>/status', views.AdminOrderStatusView.as_view()),

    # Admin bulk delete
    path('admin/bulk-delete', views.AdminBulkDeleteView.as_view()),

    # Site Settings
    path('settings/', views.SiteSettingsView.as_view()),
    path('settings/update', views.SiteSettingsUpdateView.as_view()),

    # Admin Users
    path('users/', views.AdminUsersView.as_view()),
]

