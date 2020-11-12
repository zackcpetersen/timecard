from django.contrib import admin

from projects.models import Project, ProjectImage

admin.site.register(Project, admin.ModelAdmin)
admin.site.register(ProjectImage, admin.ModelAdmin)
