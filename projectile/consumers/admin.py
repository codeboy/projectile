# -*- coding: utf-8 -*-
from django.contrib import admin

from models import ConsumerProfile


class ConsumerProfileAdmin(admin.ModelAdmin):
    save_on_top = True

admin.site.register(ConsumerProfile, ConsumerProfileAdmin)
