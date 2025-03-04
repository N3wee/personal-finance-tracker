"""
URL configuration for finance_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from transactions import views  # Import views from transactions

urlpatterns = [
    path('', views.landing_page, name='landing_page'),  # Map root to landing_page directly
    path('transactions/', include('transactions.urls')),  # Include transactions app URLs under /transactions/
    path('accounts/', include('django.contrib.auth.urls')),  # Authentication URLs
    path('register/', views.RegisterView.as_view(), name='register'),  # Registration route
    path('admin/', admin.site.urls),
    path('password_reset/', include('django.contrib.auth.urls')),  # Uses default password reset views
]