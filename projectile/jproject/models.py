# -*- coding: utf-8 -*-
# models.py for projectile

import datetime
from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

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
    project = models.ForeignKey(Project,
        verbose_name=_('Project'),)
    user = models.ForeignKey(User,
        verbose_name=_('User'))
    user_role = models.ManyToManyField('ProjectUserRoles',
        verbose_name=_('User role'))

    def __unicode__(self):
        return u'%s - %s [%s]' % (self.project, self.user, self.user_role)

    class Meta:
        verbose_name = _('Project user')
        verbose_name_plural= _('Project users')


class ProjectUserRoles(models.Model):
    """    roles for users in project    """
    USER_TYPE = (
            ('DEV', _('developer')), ('REP', _('reporter')), ('VIW', _('viewer')),
            ('TST', _('tester')),
    )
    name = models.CharField(
        max_length=225,
        verbose_name=_('Name'),
        help_text=_('executive, developer, reporter, viewer, tester'),
        unique=True,)
    name_slug = models.SlugField(
        max_length=250,
        unique=True,
        verbose_name=_('Short slug name'),)
    description = models.TextField(
        null=True, blank=True,
        verbose_name=_('Short description'),)

    r_executive = models.BooleanField(verbose_name=_('this is executive of tasks'), default=False,
                                       help_text=_('can work, report, change states'))
    r_can_create = models.BooleanField(verbose_name=_('can create'), default=False,
                                       help_text=_('full CRUD operations'))
    r_can_modif = models.BooleanField(verbose_name=_('can modificate'), default=False,
                                      help_text=_('only read and update, change states'))
    r_can_test = models.BooleanField(verbose_name=_('tester'), default=False,
                                     help_text=_('can mark tested'))
    r_can_report = models.BooleanField(verbose_name=_('can post reports'), default=False,
                                       help_text=_('can post reports'))
    r_can_view = models.BooleanField(verbose_name=_('can view'), default=False,
                                     help_text=_('this is like simple viewer'))


    def __unicode__(self):
            return self.name
    class Meta:
        verbose_name, verbose_name_plural = _('User role'), _('User roles')

    def save(self, *args, **kwargs):
        if self.name_slug is None:
            self.name_slug = slugify(self.name)
        super(ProjectUserRoles, self).save(*args, **kwargs)



class Component(models.Model):
    """
    components of project
    projects can have many of this, and task must be attached on this
    """

    name = models.CharField(
        max_length=225, unique=True,
        verbose_name=_('Name'),)
    name_slug = models.SlugField(
        max_length=250, unique=True,
        verbose_name=_('Short slug name'),)
    description = models.TextField(
        null=True, blank=True,
        verbose_name=_('Short description'),)

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

    TYPES_CHOICES = (('REL', _('Release')), ('MLS', _('Milestone')),)

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
        max_length=3,
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
        return '%s, %s' % (self.name, self.type)
    class Meta:
        verbose_name, verbose_name_plural = _('Milestone'), _('Milestones')
        unique_together = (('name', 'project'), ('name_slug', 'project'),)
    def save(self, *args, **kwargs):
        self.datetime_modifed = datetime.datetime.now()
        if self.name_slug is None:
            self.name_slug = slugify(self.name)
        super(Milestone, self).save(*args, **kwargs)