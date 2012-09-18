# -*- coding: utf-8 -*-

from django.template import Context, RequestContext
from django.template.loader import render_to_string, get_template
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from procesors import custom_processor as cp
from utils import page_message





@login_required
def index(request):
    """
    вывод
    """
    template = 'baseapp/ba-main.html'
    data = dict()

    t, c = (get_template(template), RequestContext(request,data, processors=[cp]))
    return HttpResponse(t.render(c))
