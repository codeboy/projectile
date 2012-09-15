# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms import ModelForm, Textarea, PasswordInput, EmailField

from models import Project



class ProjectEditForm(ModelForm):
#    name = forms.CharField(label='name')
#    name_slug = forms.CharField(show_hidden_initial=True, label='name', initial=True)

    class Meta:
        model = Project
#        exclude = ('name_slug')
        fields = ('name', 'description')



class MilestoneEditForm(ModelForm):
#    name = forms.CharField(label='name')
#    name_slug = forms.CharField(show_hidden_initial=True, label='name', initial=True)

    class Meta:
        model = Project
#        exclude = ('name_slug')
        fields = ('name', 'description')