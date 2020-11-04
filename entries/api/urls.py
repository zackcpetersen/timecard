from django.urls import path, include
from rest_framework import routers

from entries.api import viewsets as entries_views

router = routers.DefaultRouter()

router.register(r'entries', entries_views.EntryViewSet)
