# -*- coding: utf-8 -*-
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.utils.http import int_to_base36, base36_to_int


def confirm_url_gen(user):
    """
    Генерация ссылки токена для активации пользователя
    """

    token = default_token_generator.make_token(user)
    uid = int_to_base36(user.id)
    url = reverse('consumers:confirm-registration', args=(uid, token,))

    return url
