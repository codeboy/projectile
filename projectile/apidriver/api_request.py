from django.http import HttpRequest


# In a separate file to avoid circular imports...
class ApiRequest(object):
    """
    """
    def __init__(self, request=None):
        self.request = request or HttpRequest()

#    def __repr__(self):
#        return "<Bundle for obj: '%s' and with data: '%s'>" % (self.obj, self.data)
