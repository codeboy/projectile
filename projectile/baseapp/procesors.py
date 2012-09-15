# -*- coding: utf-8 -*-

from django.core import urlresolvers


def custom_processor(request):
    proc_data = dict()

    resolver = urlresolvers.get_resolver(None)
    patterns = sorted(
        (key, val[0][0][0]) for key, val in resolver.reverse_dict.iteritems() if isinstance(key, basestring))
    proc_data['pat'] = patterns


    proc_data['app'] = 'Common app'
    proc_data['ip_address'] = request.META['REMOTE_ADDR']
    proc_data['user'] = request.user

    return proc_data
