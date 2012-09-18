# -*- coding: utf-8 -*-
# admin.py for catalog_engine

from django.contrib import admin
from django.db.models import TextField

from projectile.jproject.models import Project, Milestone, Component, ProjectUserRoles, ProjectUsers



class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"name_slug": ("name",)}
    save_on_top = True
admin.site.register(Project, ProjectAdmin)

class MilestoneAdmin(admin.ModelAdmin):
    prepopulated_fields = {"name_slug": ("name",)}
    save_on_top = True
admin.site.register(Milestone, MilestoneAdmin)

class ComponentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"name_slug": ("name",)}
    save_on_top = True
admin.site.register(Component, ComponentAdmin)



class UserRolesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"name_slug": ("name",)}
    save_on_top = True
admin.site.register(ProjectUserRoles, UserRolesAdmin)


