from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from projects.api.serializers import ProjectImageSerializer, ProjectSerializer
from projects.models import Project, ProjectImage


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for project CRUD
    """
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectImageViewSet(viewsets.ModelViewSet):
    """
   API Endpoint for project image CRUD
   """
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImageSerializer
