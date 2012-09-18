# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns


urlpatterns = patterns('c300.adminpanel.views',
    url(r'^$', 'index', name='ap_base'),
    url(r'logout/$', 'ap_logout', name='ap_logout'),

#    url(r'api-street/(?P<type>.*)$', 'street_test', name='street_test'),
    #url(r'testapi/(?P<type>.*)$', 'testapi', name='testapi'),
    url(r'api/street/(?P<type>.*)$', 'street_api', name='street_api'),
    url(r'api/testajax/(?P<url>.*)$', 'test_ajax_to_template',
        name='test_ajax_to_template'),
    url(r'api/kladr/(?P<code>\d+)/(?P<level>[1-5])/$', 'address_list',
        name='kladr_api'),

)
