from django.urls import path, include
from rest_framework import routers

from accounts.api import viewsets as account_views

router = routers.DefaultRouter()

router.register(r'users', account_views.UserCreationViewSet)
router.register(r'update-user', account_views.UserUpdateViewSet)


urlpatterns = [
    path('accounts/', include('rest_auth.urls')),
    path('current-user/', account_views.CurrentUserGetView.as_view())
]
