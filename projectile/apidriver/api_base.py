# -*- coding: utf-8 -*-
from copy import deepcopy
from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.utils.cache import patch_cache_control

from projectile.apidriver.api_resource import ResourceOptions
from projectile.apidriver.api_request import ApiRequest

try:
    from tastypie.resources import Resource
except : pass

#--------------------------------------------------
#
#   TODO: add http.HttpAccepted()
#
#--------------------------------------------------


class DeclarativeMetaclass(type):
    """
    метакласс для BaseApi
    """
    def __new__(cls, name, bases, attrs):
        attrs['base_fields'] = {}
        declared_fields = {}

        try:
            parents = [b for b in bases if issubclass(b, BaseApi)]
            parents.reverse()

            for p in parents:
                parent_fields = getattr(p, 'base_fields', {})

                for field_name, field_object in parent_fields.items():
                    attrs['base_fields'][field_name] = deepcopy(field_object)
        except NameError:
            pass

        attrs['base_fields'].update(declared_fields)
        attrs['declared_fields'] = declared_fields
        new_class = super(DeclarativeMetaclass, cls).__new__(
            cls, name, bases, attrs)
        opts = getattr(new_class, 'Meta', None)
        new_class._meta = ResourceOptions(opts)

        return new_class


class BaseApi(object):
    __metaclass__ = DeclarativeMetaclass

    resource_name = 'test'
#    request = None
    urls = []

    def __init__(self, api_name=None):
        self.fields = deepcopy(self.base_fields)

        if not api_name is None:
            self._meta.api_name = api_name
#        print '======', self._meta.resource_name

#    def __getattr__(self, name):
#        if name in self.fields:
#            return self.fields[name]
#        raise AttributeError(name)

    #--------------------------------------------------------
    def _build_reverse_url(self, name, args=None, kwargs=None):
        """
        A convenience hook for overriding how URLs are built.
        See ``NamespacedModelResource._build_reverse_url`` for an example.
        """
        namespaced = "%s:%s" % (self._meta.urlconf_namespace, name)
        return reverse(namespaced, args=args, kwargs=kwargs)
#        return reverse(name, args=args, kwargs=kwargs)

    def base_urls(self):
        """
        The standard URLs this ``BaseApi`` should respond to.
        """
        # Due to the way Django parses URLs,
        # ``get_multiple`` won't work without
        # a trailing slash.
        return [
            url(r"^$", self.wrap_view('dispatch_default'),
                name="api_dispatch_default"),
            url(r"^base$", self.wrap_view('dispatch_default'),
                name="api_dispatch_default"),
            ]

    def override_urls(self):
        """
        A hook for adding your own URLs or overriding the default URLs.
        """
        return []

    @property
    def urls(self):
        """
        The endpoints this ``BaseApi`` responds to.
        """
        urls = self.override_urls() + self.base_urls()
        urlpatterns = patterns('',
            *urls
        )
#        print '=========================' ,urlpatterns
        return urlpatterns

    def wrap_view(self, view):
        """
        Wraps methods so they can be called in a more functional way as well
        as handling exceptions better.
        """
        @csrf_exempt
        def wrapper(request, *args, **kwargs):
            callback = getattr(self, view)
            response = callback(request, *args, **kwargs)

            if request.is_ajax():
                patch_cache_control(response, no_cache=True)

            return response
        return wrapper

    def build_bundle(self, request=None):
        """
        for now this for testing purpose
        """
        return ApiRequest(request=request)

    def create_pagination_dict(self, request, type='dict'):
        """
        обрабатываем переменые для пагинации
        """
        r_start = 0 if not request.POST.get('start') else int(request.POST.get('start'))
        r_limit = 20 if not request.POST.get('limit') else int(request.POST.get('limit'))
        r_page = 1 if not request.POST.get('page') else int(request.POST.get('page'))

        if not type == 'vars':
            paging = {'start' : r_start, 'limit' : r_limit, 'page' : r_page}
            return paging
        else:
            return r_start, r_limit, r_page



    def create_response(self, res_type=None, res_script=None, res_message=None,
                        res_success=None, res_name=None, res_data=None):
        resp_type = res_type if res_type  else self._meta.resp_type
        resp_script = res_script if res_script else self._meta.resp_script
        resp_message = res_message if res_message else self._meta.resp_message
        resp_success = res_success if res_success else self._meta.resp_success
        resource_name = res_name if res_name else self._meta.resource_name
        resp_render_data = res_data if res_data else self._meta.resp_render_data

        req = {
            'type': resp_type
            ,'success' : resp_success
            ,'message' : resp_message
            , 'script' : resp_script
            ,'data': resp_render_data
            ,'resource_name': resource_name
        }
        response = simplejson.dumps(req)
        return HttpResponse(response, mimetype="application/json")

    def dispatch_default(self, request):
        # TODO: not in use
        resp_template = self._meta.resp_template

        resp_type = self._meta.resp_type
        resp_script = self._meta.resp_script
        resp_message = self._meta.resp_message
        resp_success = self._meta.resp_success
        resource_name = self._meta.resource_name
        resp_render_data = self._meta.resp_render_data

        req = {
            'type': resp_type # тип ответа
            ,'success' : resp_success # ответ об удачной операции
            ,'message' : resp_message # сообщение
            , 'script' : resp_script
            ,'data': resp_render_data
            ,'resource_name': resource_name
        }
        response = simplejson.dumps(req)
        return HttpResponse(response, mimetype="application/json")
