from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    # type = models.ForeignKey() ??
    # status = models.CharField(choices=) ??


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='project_images')
    image = models.ImageField(upload_to='images')
    created_at = models.DateTimeField(auto_now_add=True)
