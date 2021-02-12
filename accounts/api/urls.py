from django.urls import include, path
from rest_framework import routers

from accounts.api import viewsets as account_views

router = routers.DefaultRouter()

router.register(r'users', account_views.UserCreationViewSet)
router.register(r'update-user', account_views.UserUpdateViewSet)

urlpatterns = [
    path('accounts/', include('rest_auth.urls')),
    path('current-user/', account_views.CurrentUserGetView.as_view()),
    path('reset-password/', account_views.UserResetPasswordView.as_view()),
    path('forgot-password/', account_views.UserForgotPasswordView.as_view())
]
