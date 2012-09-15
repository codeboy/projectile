# -*- coding: utf-8 -*-
# models.py for projectile

import datetime
from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from projectile.baseapp.utils import lang_stub as _

from treebeard.mp_tree import MP_Node
from projectile.consumers.models import ConsumerProfile as CustomUser
from projectile.jproject.models import Component, Milestone, Project


class Task(MP_Node):
    TASK_VISIBLES = (
        ('NON', 'no one'), ('ALL', 'all'),
        ('USR', 'user executive'), ('SUS', 'selected users'))

    TYPES_CHOICES = (('BUG', u'Баг'), ('ENC', u'Улучшение'), ('TAS', u'Задача'),)
    PRIORITIES_CHOICES = (('BLK', u'Блокирующе'), ('CRT', u'Критично'), ('MAJ', u'Важно'), ('NRM', u'Средне'),
        ('MDL', u'Слабое'), ('LOW', u'Низкое'))

    STATUS_CHOICES = (('WIT', 'waiting'), ('HLD', 'on hold'), ('WIP', 'in progress'), ('DNE', 'done'),
        ('CFD', 'confirmed'), ('CLD', 'closed'),)
    STATUS_CHOICES_RU = (('WIT', 'wait'), ('HLD', 'on hold'), ('WIP', 'in progress'), ('DNE', 'done'),
        ('CFD', 'confirmed'), ('CLD', 'closed'),)

    name = models.CharField(
        max_length=225,
        verbose_name='Название',
        help_text='название задачи',
        unique=True,)
    name_slug = models.SlugField(
        max_length=250,
        unique=True,
        verbose_name='Короткое название',
        help_text='короткое название для URL, даётся автоматом, но можно изменять',)

    type = models.CharField(
        max_length=3,
        choices=TYPES_CHOICES)
    priority = models.CharField(
        max_length=3,
        choices=PRIORITIES_CHOICES)
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES)

    time_required_int = models.PositiveSmallIntegerField(
        null=True, blank=True,
        editable=False,
        verbose_name=_('time required'),)
    time_final_int = models.PositiveSmallIntegerField(
        null=True, blank=True,
        editable=False,
        verbose_name=_('elapsed time'),)

    description = models.TextField(
        null=True, blank=True,
        verbose_name='Короткое описание',
        help_text='короткое описание',)

    datetime_created = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата внесения',)
    datetime_modified = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата изменения',)
    datetime_end = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата окончания',)

    user_author = models.ForeignKey(User,
        related_name='user_author')
    user_executive = models.ForeignKey(User,
        related_name='user_executive',
        null=True, blank=True,)

    project = models.ForeignKey(Project)
    component = models.ForeignKey(Component,
        null=True, blank=True,)
    release  = models.ForeignKey(Milestone,
        null=True, blank=True,)

    is_visible = models.CharField(
        max_length=3,
        choices=TASK_VISIBLES,
        default='ALL',
        verbose_name='Видимость таска',)

    visi_users = models.ManyToManyField(CustomUser,
        related_name='task_users',
        null=True, blank=True,)



    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural= 'Tasks'

    def save(self, *args, **kwargs):
        self.datetime_modified = datetime.datetime.now()
        if self.name_slug is None:
            self.name_slug = slugify(self.name)
        super(Task, self).save(*args, **kwargs)




class TaskStates(models.Model):

    description = models.TextField(
        null=True, blank=True,
        verbose_name='Короткое описание',
        help_text='короткое описание',)

#    task_id = models.PositiveIntegerField()
    task_id = models.ForeignKey(Task,)
    user_author = models.ForeignKey(User,)


#    def __unicode__(self):
#        return self.name

    class Meta:
        verbose_name = 'Task state'
        verbose_name_plural= 'Task states'

    def save(self, *args, **kwargs):
        self.datetime_modified = datetime.datetime.now()
        super(TaskStates, self).save(*args, **kwargs)