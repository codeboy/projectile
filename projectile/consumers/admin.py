# -*- coding: utf-8 -*-
from django.contrib import admin

from models import ConsumerProfile


class ConsumerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'snils']

admin.site.register(ConsumerProfile, ConsumerProfileAdmin)
