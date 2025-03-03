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
from transactions.views import RegisterView

urlpatterns = [
    path('', include('transactions.urls')),  # Redirect root to transactions.urls (landing_page)
    path('accounts/', include('django.contrib.auth.urls')),  # Authentication URLs
    path('register/', RegisterView.as_view(), name='register'),  # Registration route
    path('admin/', admin.site.urls),
    # Password reset URLs
    path('password_reset/', include('django.contrib.auth.urls')),  # Uses default password reset views
]