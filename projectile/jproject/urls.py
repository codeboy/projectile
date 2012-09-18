# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns


urlpatterns = patterns('projectile.jproject.views',
    url(r'^$', 'index', name='ap_base'),
)
