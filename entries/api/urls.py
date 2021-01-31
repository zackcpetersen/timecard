from django.urls import path
from rest_framework import routers

from entries.api import viewsets as entry_views

router = routers.DefaultRouter()

router.register(r'entries', entry_views.EntryViewSet)
router.register(r'update-entry', entry_views.EntryUpdateViewSet)

urlpatterns = [
    path('start-time/', entry_views.StartTimeView.as_view()),
    path('end-time/', entry_views.EndTimeView.as_view()),
    path('start-pause/', entry_views.StartPauseView.as_view()),
    path('end-pause/', entry_views.EndPauseView.as_view()),
    path('entry-download/', entry_views.EntryCSVDownloadView.as_view()),
    path('filter-entries/', entry_views.EntryFilterView.as_view()),
    path('entry-status/', entry_views.EntryStatusView.as_view())
]
