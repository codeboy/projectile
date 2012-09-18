# -*- coding: utf-8 -*-
# admin.py for catalog_engine

from django.contrib import admin
from treebeard.admin import TreeAdmin


from projectile.jtask.models import Task, TaskType, TaskPriorities, TaskStates, TypeStatusesOrder, StatusItem



class SimpleSlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {"name_slug": ("name",)}
    save_on_top = True
admin.site.register(TaskPriorities, SimpleSlugAdmin)
admin.site.register(TaskType, SimpleSlugAdmin)
admin.site.register(StatusItem, SimpleSlugAdmin)

class SimpleAdmin(admin.ModelAdmin):
    save_on_top = True
admin.site.register(TaskStates, SimpleAdmin)

class MP_Statuses_Admin(TreeAdmin):
#    pass
    save_on_top = True
admin.site.register(TypeStatusesOrder, MP_Statuses_Admin)
class MP_Tasks_Admin(TreeAdmin):
    prepopulated_fields = {"name_slug": ("name",)}
    save_on_top = True
admin.site.register(Task, MP_Tasks_Admin)