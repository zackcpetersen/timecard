from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from projects import constants as project_constants


@receiver(post_save, sender='projects.ProjectImage')
def allow_single_featured_img(sender, instance, **kwargs):
    if instance.featured:
        instance.project.project_images.exclude(pk=instance.pk).update(featured=False)


post_save.connect(allow_single_featured_img, sender='projects.ProjectImage')


class Project(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=project_constants.PROJECT_STATUSES,
                              default=project_constants.STATUS_ACTIVE,
                              max_length=255)
    type = models.ForeignKey('projects.ProjectType',
                             on_delete=models.PROTECT,
                             related_name='projects')

    def __str__(self):
        return self.name


class ProjectImage(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT,
                                related_name='project_images')
    entry = models.ForeignKey('entries.Entry',
                              on_delete=models.PROTECT,
                              related_name='entry_images',
                              blank=True, null=True)
    image = models.ImageField(upload_to='project-images')
    created_at = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProjectType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
