from django.contrib import admin

from projects.models import Project, ProjectImage, ProjectType

admin.site.register(Project, admin.ModelAdmin)
admin.site.register(ProjectImage, admin.ModelAdmin)
admin.site.register(ProjectType, admin.ModelAdmin)
