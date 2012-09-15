# -*- coding: utf-8 -*-

from django.views.generic.simple import direct_to_template
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, render, redirect
from django.template.loader import render_to_string, get_template
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#from projectile.baseapp.models import Home
from projectile.consumers.forms import ConsumerLoginForm
from procesors import custom_processor as cp
from utils import page_message


from django.template import RequestContext



@login_required
def index(request):
    """
    вывод
    """
    template = 'baseapp/ba-main.html'
    data = dict()

#    try:
#        q_company = Company.objects.get(owner = request.user)
#        data['list'] = q_company
#    except (WorkObject.DoesNotExist, Company.DoesNotExist):
#        page_message(request, 50, None, 'error')
#        return redirect('/')

    t, c = (get_template(template), RequestContext(request,data, processors=[cp]))
    return HttpResponse(t.render(c))


def ba_login(request):
    url = '/' if not request.GET.get('next') else request.GET.get('next')
    if request.user.is_authenticated():
        redirect(url)
    else:
        template = 'baseapp/ba-auth.html'
        data = dict()
        if request.method == 'POST':
            form = ConsumerLoginForm(request.POST)
            if form.is_valid():
                user = authenticate(username=form.cleaned_data['user_code'],
                    password=form.cleaned_data['user_password'])
                if user:
                    login(request, user)
                    return redirect(url)
                else:
                    page_message(request, 40, None, 'error')
                    data['message'] = 'Неправильное имя или пароль.'
                    form = ConsumerLoginForm(request.POST)
        else:
            form = ConsumerLoginForm()

        data['form'] = form
        t, c = (get_template(template), RequestContext(request,data, processors=[cp]))
        return HttpResponse(t.render(c))


def ba_logout(request):
    logout(request)
    return redirect('base:ba_base')


