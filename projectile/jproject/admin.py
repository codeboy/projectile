# -*- coding: utf-8 -*-
# admin.py for catalog_engine

from django.contrib import admin
from django.db.models import TextField

from commonapps.ckeditor.widgets import CKEditorWidget

from models import Project, Milestone, Component, Task, TaskStates



class ProjectAdmin(admin.ModelAdmin):
    formfield_overrides = {TextField: {'widget': CKEditorWidget()}}
    prepopulated_fields = {"name_slug": ("name",)}
    save_on_top = True
admin.site.register(Project, ProjectAdmin)

class MilestoneAdmin(admin.ModelAdmin):
    formfield_overrides = {TextField: {'widget': CKEditorWidget()}}
    prepopulated_fields = {"name_slug": ("name",)}
    save_on_top = True
admin.site.register(Milestone, MilestoneAdmin)

class ComponentAdmin(admin.ModelAdmin):
    formfield_overrides = {TextField: {'widget': CKEditorWidget()}}
    prepopulated_fields = {"name_slug": ("name",)}
    save_on_top = True
admin.site.register(Component, ComponentAdmin)



class TaskAdmin(admin.ModelAdmin):
    formfield_overrides = {TextField: {'widget': CKEditorWidget()}}
    prepopulated_fields = {"name_slug": ("name",)}
    save_on_top = True

admin.site.register(Task, TaskAdmin)

class TaskStatesAdmin(admin.ModelAdmin):
    formfield_overrides = {TextField: {'widget': CKEditorWidget()}}
#    prepopulated_fields = {"name_slug": ("name",)}
    save_on_top = True
admin.site.register(TaskStates, TaskStatesAdmin)
