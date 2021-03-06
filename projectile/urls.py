# -*- coding: utf-8 -*-

""" Default urlconf for c300 """
from django.conf import settings
from django.conf.urls.defaults import include, patterns, url
from django.contrib import admin
from django.views.generic.base import TemplateView
admin.autodiscover()

def bad(request):
    """ Simulates a server error """
    1 / 0


from projectile.baseapp.test_api import TestApi
api = TestApi()
from projectile.jproject.api_project import ProjectApi
project_api = ProjectApi()

urlpatterns = patterns('',
    (r'', include('projectile.baseapp.urls', namespace='base')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    #url(r'^', include('debug_toolbar_user_panel.urls')),
    (r'^bad/$', bad),

    (r'^api-test/', include(api.urls)),
    (r'^api-project/', include(project_api.urls)),
)




## In DEBUG mode, serve media files through Django.
if settings.DEBUG:
    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
