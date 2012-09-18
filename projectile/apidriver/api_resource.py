# -*- coding: utf-8 -*-

class ResourceOptions(object):
    """
    A configuration class for ``Resource``.

    Provides sane defaults and the logic needed to augment these settings with
    the internal ``class Meta`` used on ``Resource`` subclasses.
    """
    allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
    list_allowed_methods = None
    detail_allowed_methods = None
#    limit = getattr(settings, 'API_LIMIT_PER_PAGE', 20)

    urlconf_namespace = None
    default_format = 'application/json'
    filtering = {}
    ordering = []
    object_class = None
    queryset = None
    fields = []
    excludes = []
    include_resource_uri = True
    include_absolute_url = False
    always_return_data = False

    api_name = None
    resource_name = None

    resp_message = 'Good!'
    resp_script = None
    resp_success = True
    resp_template = 'adminpanel/ap-test.html'
    resp_type = 'tpl'
    resp_render_data = None

    make_function = None


    def __new__(cls, meta=None):
        overrides = {}

        # Handle overrides.
        if meta:
            for override_name in dir(meta):
                # No internals please.
                if not override_name.startswith('_'):
                    overrides[override_name] = getattr(meta, override_name)

        allowed_methods = overrides.get('allowed_methods', ['get', 'post', 'put', 'delete', 'patch'])

        if overrides.get('list_allowed_methods', None) is None:
            overrides['list_allowed_methods'] = allowed_methods

        if overrides.get('detail_allowed_methods', None) is None:
            overrides['detail_allowed_methods'] = allowed_methods

        return object.__new__(type('ResourceOptions', (cls,), overrides))
