# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, redirect, \
                                render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.http import base36_to_int
from django.views.decorators.csrf import csrf_protect, requires_csrf_token

from forms import ConsumerLoginForm, ConsumerRegisterForm, ActivationForm
from models import ConsumerProfile
from utils import confirm_url_gen

from c300.sender.tools import SendMessage


@login_required
def home(request):
    """ Default view for the root """

    user = request.user if request.user.is_authenticated() else None
    form = ConsumerLoginForm()

    alert = request.session.get('alert', None)
    if alert:
        del request.session['alert']

    cntx_dict = {
        'form': form,
        'alert': alert,
        'user': user
    }

    return render_to_response('consumers/home.html',
        cntx_dict,
        context_instance=RequestContext(request))


@requires_csrf_token
def registration(request):
    if request.POST:
        form = ConsumerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.is_active = False
            user.save()

            profile_data = {
                'snils': form.cleaned_data.get('snils', None),
            }

            profile = ConsumerProfile(**profile_data)
            profile.user = user
            profile.save()

            c = {
                'activate_url': unicode(request.build_absolute_uri(
                    confirm_url_gen(user))),
                'profile': profile
            }

            subject = render_to_string(
                'consumers/registration_email_subject.txt', c)
            subject = ''.join(subject.splitlines())
            message = render_to_string(
                'consumers/registration_email_body.txt', c)

            SendMessage(**{
                'sender': settings.DEFAULT_FROM_EMAIL,
                'text_message': message,
                'recipient': (user.email,),
                'subject': subject
            })

            return redirect('consumers:registration_confirm_email')
    else:
        form = ConsumerRegisterForm()

    cntx_dict = {
        'form': form,
    }
    cntx_dict.update(csrf(request))

    return render_to_response('consumers/register.html',
                               cntx_dict,
                               context_instance=RequestContext(request))


def confirm_reg(request, uidb36, token):
    """
    Проверка токена и отправка администратору уведомления
    """
    try:
        uid_int = base36_to_int(uidb36)
    except ValueError:
        raise Http404(u'Ошибка активации')

    user = get_object_or_404(User, id=uid_int)

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        profile = user.get_profile()
        profile.activate = True
        profile.save()

        request.session['alert'] = u'Ваша учетная запись активирована.'

        return redirect('consumers:home')
    else:
        raise Http404(u'Ошибка активации')


@csrf_protect
def user_login(request):
    """
    Вход
    """
    if request.user.is_authenticated():
        return redirect('base:home')

    alert = request.session.get('alert', None)
    if alert:
        del request.session['alert']

    if request.method == 'POST':
        form = ConsumerLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['user_code'],
                                password=form.cleaned_data['user_password'])
            if user:
                login(request, user)
                return redirect('consumers:home')
    else:
        form = ConsumerLoginForm()

    ctx = {
        'form': form,
        'alert': alert
    }
    ctx.update(csrf(request))
    return render_to_response('consumers/login.html', ctx,
                                context_instance=RequestContext(request))


@csrf_protect
def reset_password(request):
    """
    Сброс пароля
    """
    return password_reset(request,
        template_name='consumers/password_reset_form.html',
        post_reset_redirect=reverse('consumers:password-reset-done'),
        email_template_name='consumers/password_reset_email.html')


def password_reset_done(request):
    """
    Инструкции были отправлены
    """
    return password_reset_confirm(request,
        template_name='consumsers/password_reset_done.html')


def password_reset_complete(request):
    """
    Пароль успешно изменён
    """
    login_url = reverse('consumers:home')

    return render(request, 'consumers/password_reset_complete.html',
                  {'login_url': login_url})


def password_confirm(request, uidb36, token):
    """
    Создание нового пароля
    """
    return password_reset_confirm(request,
        uidb36=uidb36,
        token=token,
        template_name='consumers/password_reset_confirm.html',
        post_reset_redirect=reverse('consumers:password_send'),
        extra_context={'uidb36': uidb36, 'token': token}
    )


def user_logout(request):
    """
    Выход
    """
    logout(request)
    return redirect('consumers:home')


def tenand_worker_register(request):
    """
    Регистрация пользователя/сотрудника
    """
    form_valid = False

    if request.method == 'POST':
        form = ActivationForm(request.POST)
        if form.is_valid():
            form_valid = True
    else:
        form = ActivationForm()

    return render(request, 'consumers/tenand_worker_registration.html',
        {
            'form': form,
            'form_valid': form_valid,
        }
    )
