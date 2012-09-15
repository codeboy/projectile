# -*- coding: utf-8 -*-
"""urlconf for the base application"""

from django.conf.urls.defaults import url, patterns


urlpatterns = patterns('projectile.baseapp.views',
    url(r'^$', 'index', name='ba_base'),

    url(r'login/$', 'ba_login', name='ba_login'),
    url(r'logout/$', 'ba_logout', name='ba_logout'),
)
