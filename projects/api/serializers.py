from rest_framework import serializers
from projects.models import Project, ProjectImage, ProjectType


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    project_images = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = '__all__'
