from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # type = models.ForeignKey() ??
    # status = models.CharField(choices=) ??

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
