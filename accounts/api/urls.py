from django.urls import path, include
from rest_framework import routers

from accounts.api import viewsets as account_views

router = routers.DefaultRouter()

urlpatterns = [
    path('accounts/', include('rest_auth.urls')),
]

router.register(r'users', account_views.UserViewSet)
