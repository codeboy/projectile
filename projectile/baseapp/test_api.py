# -*- coding: utf-8 -*-

from django.template.loader import render_to_string
from django.conf.urls.defaults import url

from projectile.apidriver.api_base import BaseApi

from projectile.jproject.models import Project


class TestApi(BaseApi):
    class Meta:
        """
        через метакласс можно задавать параметры для всего api
        но их так же можно задать\переопределить и в обработчиках
        """
        resource_name = 'Test api'

        resp_template = 'baseapp/api-test.html'
#        resp_type = 'tpl'
#        resp_script = 'ap-test.js'
        resp_message = 'good'
        resp_success = True

        data = dict()
        data['test'] = 'All good!!!'

        resp_render_data = render_to_string(resp_template, data)

    # добавляем свой урл
    def override_urls(self):
        return [
            url(r"^test$", self.test_custom_dispatch, name="api_dispatch_user"),
            url(r"^reload-test$", self.test_reload_tab, name="test_reload_tab"),
        ]


    def test_custom_dispatch(self, request):
        """
        обработчик урла (диспетчер)
        здесь мы работаем с реквестом
        """

        template = 'baseapp/api-test.html'
        data = dict()
        data['test'] = 'All FUCKIN GOOD!'
        render_data = render_to_string(template, data)

        return self.create_response(res_data=render_data)


    def test_reload_tab(self, request):
        """
        перезагрузка вкладки
        """

        template = 'adminpanel/ap-test2.html'
        data = dict()
        data['test'] = 'Вкладка перезагружена!'
        render_data = render_to_string(template, data)

        return self.create_response(res_data=render_data)

