#-*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, check_password


from django.contrib.auth.backends import ModelBackend
from django.db.models import get_model
from django.core.exceptions import ImproperlyConfigured
from models import ConsumerProfile



class ConsumerBackend(ModelBackend):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.
    """

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


    def get_mail(self, user_id):
        try:
            return self.user_class.objects.get(pk=user_id)
        except self.user_class.DoesNotExist:
            return None


#    @property
#    def user_class(self):
#        if not hasattr(self, '_user_class'):
#            self._user_class = get_model(*settings.CUSTOM_USER_MODEL.split('.', 2))
#            if not self._user_class:
#                raise ImproperlyConfigured('Could not get custom user model')
#        return self._user_class





