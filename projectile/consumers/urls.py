# -*- coding: utf-8 -*-
"""urlconf for the consumers application"""

from django.conf.urls.defaults import url, patterns, include
from django.views.generic import TemplateView

from api import ConsumerApi

api = ConsumerApi()

urlpatterns = patterns('c300.consumers.views',
    url(r'^$', 'home', name='home'),
    url(r'api/', include(api.urls)),
    url(r'login/$', 'user_login', name='login'),
    url(r'logout/$', 'user_logout', name='logout'),
    url(r'registration/$', 'registration', name='registration'),
    url(r'^registration/confirm/([\w\-]+)/([\w\-]+)/$', 'confirm_reg',
        name='confirm-registration'),
    url(r'^registration/confirm/email/$',
        TemplateView.as_view(template_name='consumers/registration_confirm.html'),
        name='registration_confirm_email'
    ),
    url(r'^password/reset/done/$',
        TemplateView.as_view(template_name='consumers/password_reset_done.html'),
        name='password-reset-done'
    ),
    url(r'reset_password/$', 'reset_password', name='reset_password'),
    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'password_confirm', name='password_confirm'),
    url(r'^password/reset/send/$', 'password_reset_complete',
        name='password_send'),
)

urlpatterns += patterns('c300.consumers.views',
    url(r'activate/$', 'tenand_worker_register',
        name='activate_tenand_worker'),
)
