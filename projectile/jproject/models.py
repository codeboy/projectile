# -*- coding: utf-8 -*-
# models.py for projectile

import datetime
from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from treebeard.mp_tree import MP_Node

from projectile.baseapp.utils import lang_stub as _
from projectile.consumers.models import ConsumerProfile as CustomUser


class Project(models.Model):
    PROJECT_VISIBLES = (
        ('NON', 'no one'), ('ALL', 'all'),
        ('USR', 'user'), ('SUS', 'selected users'))

    owner = models.ForeignKey(CustomUser,
        related_name='owner')
    creator = models.ForeignKey(CustomUser,
        related_name='creator')

    name = models.CharField(
        max_length=225,
        verbose_name='Название',
        help_text='название проекта',
        unique=True,)
    name_slug = models.SlugField(
        max_length=250,
        unique=True,
        verbose_name='Короткое название',
        help_text='короткое название для URL',)

    description = models.TextField(
        null=False, blank=False,
        verbose_name='Короткое описание',
        help_text='короткое описание',)

    datetime_created = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата создания',)
    datetime_modifed = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата изменения',)
#    logo = models.ForeignKey(Image,
#        null=True, blank=True,)

    is_visible = models.CharField(
        max_length=3,
        choices=PROJECT_VISIBLES,
        default='ALL',
        verbose_name='Видимость проекта',)
    is_active = models.BooleanField(
        default=True,
        verbose_name='активность',
        help_text='false запрещает создание новых данных')

#    users = models.ManyToManyField(CustomUser,
#        related_name='prj_users',
#        null=True, blank=True,)


    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural= 'Проекты'


    def save(self, *args, **kwargs):
        self.datetime_modifed = datetime.datetime.now()
        if self.name_slug is None:
            self.name_slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)


class ProjectUsers(models.Model):
    """
    project users
    """
    USER_TYPE = (
            ('DEV', _('developer')), ('REP', _('reporter')), ('VIW', _('viewer')),
            ('TST', _('tester')), ('REP', _('reporter')),
    )
    project = models.ForeignKey(Project,
        verbose_name=_('Project'),)
    user = models.ForeignKey(User,
        verbose_name=_('User'))
    user_type = models.CharField(
        max_length=3,
        choices=USER_TYPE,
        verbose_name=_('User type'),
    )

    def __unicode__(self):
        return u'%s - %s [%s]' % (self.project, self.user, self.user_type)

    class Meta:
        verbose_name = _('Project user')
        verbose_name_plural= _('Project users')


class Component(models.Model):

    name = models.CharField(
        max_length=225,
        verbose_name='Название',
        help_text='название компонента',
        unique=True,)
    name_slug = models.SlugField(
        max_length=250,
        unique=True,
        verbose_name='Короткое название',
        help_text='короткое название для URL, даётся автоматом, но можно изменять',)

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Короткое описание',
        help_text='короткое описание',)

    datetime_created = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата внесения',)
    datetime_modifed = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата изменения',)

    project = models.ForeignKey(Project)


    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = 'Компонент'
        verbose_name_plural= 'Компоненты'


    def save(self, *args, **kwargs):
        self.datetime_modifed = datetime.datetime.now()
        if self.name_slug is None:
            self.name_slug = slugify(self.name)

        super(Component, self).save(*args, **kwargs)



# TODO: сделать необязательное поле для времени релиза
class Milestone(models.Model):

    TYPES_CHOICES = (('RE', u'Релиз'), ('MS', u'Веха'),)

    name = models.CharField(
        max_length=225,
        verbose_name='Название',
        help_text='название проекта',
#        unique=True,
        )
    name_slug = models.SlugField(
        max_length=250,
#        unique=True,
        verbose_name='Короткое название',
        help_text='короткое название для URL, даётся автоматом, но можно изменять',)

    type = models.CharField(
        max_length=2,
        choices=TYPES_CHOICES,
        default='RE')

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Короткое описание',
        help_text='короткое описание',)

    datetime_created = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата внесения',)
    datetime_modifed = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата изменения',)
    datetime_release = models.DateTimeField(
        verbose_name='Дата выпуска',)

    project = models.ForeignKey(Project)


    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = 'Выпуск'
        verbose_name_plural= 'Выпуски'
        unique_together = (('name', 'project'), ('name_slug', 'project'),)


    def save(self, *args, **kwargs):
        self.datetime_modifed = datetime.datetime.now()
        if self.name_slug is None:
            self.name_slug = slugify(self.name)

        super(Milestone, self).save(*args, **kwargs)