# -*- coding: utf-8 -*-

from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response, render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson
from django.core import serializers
from django.views.decorators.http import require_http_methods, condition
from django.contrib.auth import authenticate, login, logout

#from c300.maperbase.models import Doma, Street
from c300.maperbuildings.models import Home
from c300.maperbase.models import list_level
from c300.providers.models import CommonDepartmentCatalog, Provider

from api_buildings import BuildingsApi


from c300.consumers.forms import ConsumerLoginForm
from django.template import RequestContext




def index(request):
    if request.user.is_authenticated():
        return direct_to_template(request, 'adminpanel/ap-main.html')
    else:
        data = dict()
        if request.method == 'POST':
            form = ConsumerLoginForm(request.POST)
            if form.is_valid():
                user = authenticate(username=form.cleaned_data['user_code'],
                    password=form.cleaned_data['user_password'])
                if user:
                    login(request, user)
                    return direct_to_template(request, 'adminpanel/ap-main.html')
                else:
                    data['message'] = 'Неправильное имя или пароль.'
                    form = ConsumerLoginForm(request.POST)
        else:
            form = ConsumerLoginForm()

        data['form'] = form
        return render_to_response('adminpanel/ap-auth.html', data, context_instance=RequestContext(request))

def ap_logout(request):
    logout(request)
    return redirect('adminpanel:ap_base')




# TODO: DEPRICATED?!?!
#@require_http_methods(['POST'])
def street_api(request, type):
    """
    вывод улиц для редактирования
    """
#    print request.POST
#    print request.GET
#    print type

    r_start = 0 if not request.POST.get('start') else int(request.POST.get('start'))
    r_limit = 20 if not request.POST.get('limit') else int(request.POST.get('limit'))
    r_page = 1 if not request.POST.get('page') else int(request.POST.get('page'))

    q = Home.objects.all().order_by('id')[r_start:r_limit*r_page]
    q_count = Home.objects.all().count()

    # делаем массив данных для таблицы
    q_array = []
    for i in q:
        q_array.append({
            'id': i.pk
            ,'kladr_code': i.kladr_code
            ,'home_number': i.home_number
            ,'korpus' : i.korpus
            ,'stroenie' : i.stroenie
            ,'cache_street' : i.cache_street
        })

    # создаём json массив для ответа
    req = {
        'type': 'grid' # тип ответа
        ,'success' : True # ответ об удачной операции
        ,'message' : 'message' # сообщение
        ,'data': {
            'totalcount' : q_count # колличество записей
            ,'records': q_array # записи
        }
    }
    response = simplejson.dumps(req)

    return HttpResponse(response, mimetype="application/json")



@require_http_methods(['POST'])
def menu_list(request, type):
    """
    """

    menu = (
            {'name': 'fdsfsdf', 'url': 'dasdasd'}
        )
    req = {
        'menu' : menu,
        'message': 'ok'
    }
    response = simplejson.dumps(req)

    return HttpResponse(response, mimetype="application/json")



@require_http_methods(['POST'])
def test_ajax_to_template(request, url):
    """
    NEED COMMENT
    """
    render_data = {}
    req_script = 'testTab.js'

    if url == 'test_url':
        render_data = _return_test1(request)
    elif url == 'address':
        render_data = address_list(request, '00000000000', 1)
    elif url == 'buldings':
        render_data, req_script = _return_buildings(request)
        brrr = BuildingsApi()
        print brrr.return_text('dsadsadasdadasdasdasdsad dsadasda dsadasd')
#        render_data, req_script = BuildingsApi.return_buildings(request)

    elif url == 'providers_stuff_class':
        render_data = _return_provider_common_departments(request)
    elif url == 'providers_list':
        render_data = _return_provider_list(request)

    else:
        render_data = _return_default(request)

    # формируем словарь для ответа
    req = {
        'type': 'tpl' # тип ответа
        ,'success' : True # ответ об удачной операции
        ,'message' : 'message' # сообщение
        , 'script' : req_script
        ,'data': render_data
    }
    response = simplejson.dumps(req)

    return HttpResponse(response, mimetype="application/json")


def _return_test1(request):
    """
    NEED COMMENT
    """
    template = 'adminpanel/ap-test.html'
    data = dict()
    data['test'] = 'All good!'

    r_start = 0 if not request.POST.get('start') else int(request.POST.get('start'))
    r_limit = 20 if not request.POST.get('limit') else int(request.POST.get('limit'))
    r_page = 1 if not request.POST.get('page') else int(request.POST.get('page'))

    q = Home.objects.all().order_by('id')[r_start:r_limit*r_page]
    q_count = Home.objects.all().count()

    # делаем массив данных для таблицы
    q_array = []
    for i in q:
        q_array.append({
            'id': i.pk
            ,'kladr_code': i.kladr_code
            ,'home_number': i.home_number
            ,'korpus' : i.korpus
            ,'stroenie' : i.stroenie
            ,'cache_street' : i.cache_street
        })

    # рендер данных в шаблон
    render_data = render_to_string(template, data)

    return render_data


def _return_provider_common_departments(request):
    """
    NEED COMMENT
    """
    template = 'adminpanel/provider-common-departments.html'
    data = dict()
    data['title'] = u'Классификатор отделов и должностей'

    departments = CommonDepartmentCatalog.objects.filter(depth=1)
    q_array=[]
    for department in departments:
        q_array.append({
                'id': department.id,
                'name_slug': department.name_slug,
                'name_full': department.name_full,
                'children': department.get_children()
            })

    data['grid'] = q_array

    # рендер данных в шаблон
    render_data = render_to_string(template, data)

    return render_data


def address_list(request, code, level):
    """
    NEED COMMENT
    """
    template = 'adminpanel/ap-address.html'

    levels = {1: [1], 2: [3], 3: [2, 3, 4, 5], 4: [4], 5: [5]}
    levels_up = {1: 3, 2: 4, 3: 5, 4: 5, 5: 6}
    levels_down = {5: 3, 4: 3, 3: 1, 2: 1, 1: 1}

    int_level = int(level)
    cur_level = levels[int_level]
    prev_level = levels_down[int_level]

    obj_list = []
    for lev in cur_level:
        obj_list += [(p[0], p[1] + ', ' + p[2], levels_up[lev]) for p in list_level(code, lev)]
    data = {
        'obj_list': obj_list,
        'level': level,
        'code': code,
        'prev_level': prev_level
    }
    render_data = render_to_string(template, data)
    return render_data


def _return_provider_list(request):
    """
    NEED COMMENT
    """
    template = 'adminpanel/provider-list.html'
    data = dict()
    data['title'] = u'Список организаций'

    r_start = 0 if not request.POST.get('start') else int(request.POST.get('start'))
    r_limit = 20 if not request.POST.get('limit') else int(request.POST.get('limit'))
    r_page = 1 if not request.POST.get('page') else int(request.POST.get('page'))

    providers = Provider.objects.all()[r_start:r_limit*r_page]
    q_array=[]
    for provider in providers:
        q_array.append({
                'provider': provider
            })

    data['grid'] = q_array

    # рендер данных в шаблон
    render_data = render_to_string(template, data)

    return render_data


def _return_default(request):
    """
    NEED COMMENT
    """
    template = 'adminpanel/ap-default.html'
    data = dict()
    data['test'] = 'All good!'


    # рендер данных в шаблон
    render_data = render_to_string(template, data)

    return render_data


def _return_buildings(request):
    """
    NEED COMMENT
    """
    template = 'adminpanel/ap-buildings-list.html'
    data = dict()
    data['title'] = u'Список домов'

    r_start = 0 if not request.POST.get('start') else int(request.POST.get('start'))
    r_limit = 20 if not request.POST.get('limit') else int(request.POST.get('limit'))
    r_page = 1 if not request.POST.get('page') else int(request.POST.get('page'))

    builds = Home.objects.all().order_by('id')[r_start:r_limit*r_page]
#    q_array=[]
#    for i in builds:
#        q_array.append({
#            'provider': provider
#        })

    data['grid'] = builds

    # рендер данных в шаблон
    render_data = render_to_string(template, data)

    return render_data, 'ap-test.js'


# -----------------------------------------------
# заготовка для AJAX запроса
def ajax_template(request, type):
    error_msg = 'Get the hell out from here!'
    if not request.is_ajax(): return HttpResponse(error_msg, mimetype="application/json")
    else:
        if request.method == 'GET':
            return HttpResponse(error_msg, mimetype="application/json")

        elif request.method == 'POST':
            return HttpResponse('Good move boy.', mimetype="application/json")
