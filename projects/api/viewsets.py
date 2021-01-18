from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from projects.api.serializers import ProjectImageSerializer, ProjectSerializer, ProjectTypeSerializer
from projects.models import Project, ProjectImage, ProjectType


class AuthenticatedAPIView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ProjectViewSet(AuthenticatedAPIView):
    """
    API Endpoint for project CRUD
    """
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer


class ProjectImageViewSet(AuthenticatedAPIView):
    """
    API Endpoint for project image CRUD
    """
    queryset = ProjectImage.objects.all().order_by('-id')
    serializer_class = ProjectImageSerializer


class ProjectTypeViewSet(AuthenticatedAPIView):
    """
    API Endpoint for project type crud
    """
    queryset = ProjectType.objects.all().order_by('-id')
    serializer_class = ProjectTypeSerializer
