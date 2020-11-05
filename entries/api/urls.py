from django.urls import path, include
from rest_framework import routers

from entries.api import viewsets as entry_views

router = routers.DefaultRouter()

router.register(r'entries', entry_views.EntryViewSet)

urlpatterns = [
    path('start-time/', entry_views.StartTimeView.as_view())
]
