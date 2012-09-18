# -*- coding: utf-8 -*-
# models.py for projectile

import datetime
from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db import transaction

from projectile.baseapp.utils import lang_stub as _

from treebeard.mp_tree import MP_Node
from projectile.consumers.models import ConsumerProfile as CustomUser
from projectile.jproject.models import Component, Milestone, Project, ProjectUserRoles


class Task(MP_Node):
    TASK_VISIBLES = (
        ('NON', 'no one'), ('ALL', 'all'),
        ('USR', 'user executive'), ('SUS', 'selected users'))

#    TYPES_CHOICES = (('BUG', u'Баг'), ('ENC', u'Улучшение'), ('TAS', u'Задача'),)
    PRIORITIES_CHOICES = (('BLK', u'Блокирующе'), ('CRT', u'Критично'), ('MAJ', u'Важно'), ('NRM', u'Средне'),
        ('MDL', u'Слабое'), ('LOW', u'Низкое'))

    STATUS_CHOICES = (('WIT', 'waiting'), ('HLD', 'on hold'), ('WIP', 'in progress'), ('DNE', 'done'),
        ('CFD', 'confirmed'), ('CLD', 'closed'),)

    name = models.CharField(
        max_length=225,
        verbose_name=_('Name'),
        help_text=_('task name'),
        unique=True,)
    name_slug = models.SlugField(
        max_length=250,
        unique=True,
        verbose_name=_('Short slug name'),)

    type = models.ForeignKey('TaskType',
        verbose_name=_('Task type'))
    status = models.ForeignKey('StatusItem',
        verbose_name=_('Current status'),)
    priorities = models.ForeignKey('TaskPriorities',
    verbose_name=_('Importance of task'),)

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
        verbose_name='Short description',)

    datetime_created = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name=_('Create time'),)
    datetime_modified = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name=_('Modified time'),)
    datetime_end = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name=_('Expiration date'),)

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
        verbose_name=_('Visibility of task'),)

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
    """
    states changes - saves when something changed in task
    """
    project = models.ForeignKey(Project,
    verbose_name=_('Project'))
    description = models.TextField(
        null=True, blank=True,
        verbose_name=_('Short description'),)
    task_id = models.ForeignKey(Task,)
    user_author = models.ForeignKey(User,)

#    def __unicode__(self):
#        return self.name

    class Meta:
        verbose_name = _('Task state')
        verbose_name_plural= _('Task states')

#    def save(self, *args, **kwargs):
#        self.datetime_modified = datetime.datetime.now()
#        super(TaskStates, self).save(*args, **kwargs)


class TaskPriorities(models.Model):
    """    priorities for tasks    """
    name = models.CharField(
        max_length=225,
        verbose_name=_('Name'),
        help_text=_('set name'),
        unique=True,)
    name_slug = models.SlugField(
        max_length=250,
        unique=True,
        verbose_name=_('Short name'),
        help_text=_('short name for URL'),)
    importance = models.PositiveSmallIntegerField(
        verbose_name=_('value of importance')
    )

    class Meta:
        verbose_name = _('Task priority')
        verbose_name_plural= _('Task priorities')

    def save(self, *args, **kwargs):
        if self.name_slug is None:
            self.name_slug = slugify(self.name)
        super(TaskPriorities, self).save(*args, **kwargs)



class TaskType(models.Model):
    """
        task type
        contain set of statuses with order
    """
    project = models.ForeignKey(Project,
        verbose_name=_('Project'),)
    name = models.CharField(
        max_length=225,
        verbose_name=_('Name'),
        help_text=_('set name'),
        unique=True,)
    name_slug = models.SlugField(
        max_length=250,
        unique=True,
        verbose_name=_('Short name'),
        help_text=_('short name for URL'),)
    statuses = models.ForeignKey('TypeStatusesOrder',
        verbose_name=_('list of statuses'))

    def __unicode__(self):
        return '%s - %s' % (self.name, self.project)
    class Meta:
        verbose_name = _('Statuses Set')
        verbose_name_plural = _('Statuses sets')

    def save(self, *args, **kwargs):
        if self.name_slug is None:
            self.name_slug = slugify(self.name)
        super(TaskType, self).save(*args, **kwargs)


# TODO: update treebeard and clean
class TypeStatusesOrder(MP_Node):
    """
    order for statuses
    """
    status = models.ForeignKey('StatusItem',
        null=True, blank=True,
        verbose_name=_('status'))
    user_role = models.ManyToManyField(ProjectUserRoles,
        related_name='user_r',
        verbose_name=_('roles who can set'))

    def __unicode__(self):
        return u'%s' % self.status
    class Meta:
            verbose_name = _('Order of status')
            verbose_name_plural = _('Order of status')

#    @classmethod
#    def add_root(cls, **kwargs):
#        """
#        Adds a root node to the tree.
#        :raise PathOverflow: when no more root objects can be added
#        """
#
#        # do we have a root node already?
#        last_root = cls.get_last_root_node()
#
#        if last_root and last_root.node_order_by:
#            # there are root nodes and node_order_by has been set
#            # delegate sorted insertion to add_sibling
#            return last_root.add_sibling('sorted-sibling', **kwargs)
#
#        if last_root:
#            # adding the new root node as the last one
#            newpath = cls._inc_path(last_root.path)
#        else:
#            # adding the first root node
#            newpath = cls._get_path(None, 1, 1)
#        # Pop ManyToManyFields to add them later
#        m2m = {}
#        for field in cls._meta.many_to_many:
#            if field.name not in kwargs:
#                continue
#            m2m[field.name] = kwargs.pop(field.name)
#
#        # creating the new object
#        newobj = cls(**kwargs)
#        newobj.depth = 1
#        newobj.path = newpath
#        # saving the instance before returning it
#        newobj.save()
#        # save m2m
#        for field, value in m2m.items():
#            setattr(newobj, field, value)
#        newobj.save()
#        transaction.commit_unless_managed()
#        return newobj


class StatusItem(models.Model):
    """
    task statuses
    """
    name = models.CharField(
        max_length=225,
        verbose_name=_('Name'),
        help_text=_('status name'),
        unique=True,)
    name_slug = models.SlugField(
        max_length=250,
        unique=True,
        verbose_name=_('Short name'),
        help_text=_('short name for URL'),)

    type = models.CharField(
        max_length=3,)

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = _('Task status item')
        verbose_name_plural= _('Task status items')

    def save(self, *args, **kwargs):
        if self.name_slug is None:
            self.name_slug = slugify(self.name)
        super(StatusItem, self).save(*args, **kwargs)