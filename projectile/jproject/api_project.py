# -*- coding: utf-8 -*-

from django.template.loader import render_to_string
from django.conf.urls.defaults import url

from projectile.apidriver.api_base import BaseApi

from projectile.jproject.models import Project
from projectile.jtask.models import Task


class ProjectApi(BaseApi):
    class Meta:
        """
        через метакласс можно задавать параметры для всего api
        но их так же можно задать\переопределить и в обработчиках
        """
        resource_name = 'Test api'

        resp_template = 'baseapp/api-test.html'
#        resp_type = 'tpl'
#        resp_script = 'jproject/js/jp-task-list.js'
        resp_message = 'good'
        resp_success = True

        data = dict()
        data['test'] = 'All good!!!'

        resp_render_data = render_to_string(resp_template, data)

    # добавляем свой урл
    def override_urls(self):
        return [
            url(r"^base$", self.projects_base, name="api_projects_base"),
            url(r"^project/(?P<project_name>.*)$", self.project_view, name="api_project_view"),
#            url(r"^reload-test$", self.test_reload_tab, name="test_reload_tab"),
        ]


    def projects_base(self, request):
        """
        base api resource for projects
        """
        template = 'jproject/api-jp-base.html'
        data = dict()
        data['page_name'] = 'Projects list'

        q = Project.objects.all()
        data['list'] = q
        render_data = render_to_string(template, data)

        return self.create_response(res_data=render_data)


    def project_view(self, request, project_name):
        """
        show project
        """
        template = 'jproject/api-jp-project-view.html'
        data = dict()
        q = Project.objects.get(name_slug = project_name)
        data['project'] = q
        data['page_name'] = q.name

        task_list = Task.objects.filter(project = q)
        data['task_list'] = task_list
        render_data = render_to_string(template, data)

        return self.create_response(res_data=render_data)


    def add_task(self, request, project_name):
            """
            add task in project
            """
            template = 'jproject/api-jp-project-view.html'
            data = dict()
            q = Project.objects.get(name_slug = project_name)
            data['project'] = q
            data['page_name'] = q.name

            task_list = Task.objects.filter(project = q)
            data['task_list'] = task_list
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

