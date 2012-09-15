# -*- coding: utf-8 -*-
from django import forms


class ConsumerLoginForm(forms.Form):
    """
    Форма для входа пользователей
    """
    user_code = forms.CharField(required=True, max_length=50,
                                label=u'Введите имя')
    user_password = forms.CharField(required=True, max_length=15,
                                    widget=forms.PasswordInput(),
                                    label=u'Введите пароль')
