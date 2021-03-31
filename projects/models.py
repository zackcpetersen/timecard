from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models.constraints import UniqueConstraint
from io import StringIO
from PIL import ImageOps, Image

from projects import constants as project_constants

@receiver(pre_save, sender='projects.ProjectImage')
def fix_image_orientation(sender, instance, **kwargs):
    if not instance.pk:
        image = Image.open(instance.image)
        image = ImageOps.exif_transpose(image)
        image.save(instance.image)
        image.close()


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
    name = models.CharField(max_length=50)
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

    class Meta:
        constraints = [UniqueConstraint(fields=['name', 'project'], name='unique_proj_img')]

    def __str__(self):
        return self.name


class ProjectType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
