#-*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class ConsumerProfile(models.Model):
    """
    User profile
    """
    user = models.OneToOneField(User, related_name='profile')
    activate = models.BooleanField(verbose_name=_('Activated'),
                                   default=False)
    skype = models.CharField(_('skype'), max_length=50, blank=True)


    class Meta:
        verbose_name = u'Профиль'
        verbose_name_plural = u'Профили'

    def __unicode__(self):
        return self.user.username

    def get_full_name(self):
        """
        get user full name
        """
        if self.user.first_name and self.user.last_name:
            return u'%s %s' % (self.user.first_name, self.user.last_name)
        else:
            return self.user.username

    def store_record(self):
        return {
            'id': self.id,
            'name': self.user.username
        }


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ConsumerProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
