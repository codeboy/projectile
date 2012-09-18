# -*- coding: utf-8 -*-
from c300.adminpanel.api_base import BaseApi
from django.template.loader import render_to_string
from django.conf.urls.defaults import url

from c300.maperbuildings.models import Home


class TestApi(BaseApi):
    class Meta:
        """
        через метакласс можно задавать параметры для всего api
        но их так же можно задать\переопределить и в обработчиках
        """
        resource_name = 'Test api'

        resp_template = 'adminpanel/ap-test-pagination.html'
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
            url(r"^test-table-pagination$", self.test_table_pagination, name="table_pagination"),
            url(r"^test_create_table$", self._create_table, name="test_create_table"),
        ]


    def test_custom_dispatch(self, request):
        """
        обработчик урла (диспетчер)
        здесь мы работаем с реквестом
        """

        template = 'adminpanel/ap-test2.html'
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



    def test_table_pagination(self, request):
        """
        тест пагинации
        """

        table = self._create_table(self.create_pagination_dict(request))

        template = 'adminpanel/ap-test-pagination.html'
        data = dict()
        data['title'] = 'тестовая страница для пагинации'
        data['table_url'] = 'test_create_table'
        data['table'] = table
        render_data = render_to_string(template, data)

        return self.create_response(res_data=render_data)


    def _create_table(self, pag):
        """
        пример создания таблицы
        """
        q = Home.objects.all().order_by('id')[pag['start']:pag['limit']*pag['page']]
        q_count = Home.objects.all().count()

        # делаем массив данных для таблицы
        q_array = []
        for i in q:
            q_array.append({
                'id': i.pk,
                'number': i.home_number,
                'corp': i.korpus,
                'street': i.cache_street
            })

        pag_dict = dict()
        pag_dict['pag_current'] = pag['page']
        pag_dict['pag_pages'] = q_count/pag['limit']

        template = 'adminpanel/ap-prt-table.html'
        data = dict()
        data['list'] = q_array
        data['count'] = q_count
        data['pagination'] = pag_dict

        render_data = render_to_string(template, data)

        return render_data