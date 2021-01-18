from rest_framework import serializers
from projects.models import Project, ProjectImage, ProjectType


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    project_images = ProjectImageSerializer(many=True, read_only=True)
    type_name = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_type_name(self, project):
        return project.type.name


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = '__all__'
