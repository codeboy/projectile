# -*- coding: utf-8 -*-

from django.template.loader import render_to_string

from c300.maperbuildings.models import Home

class BuildingsApi(object):

    def __init__(self):
#        self.return_text(text)
        pass

    def return_text(self, text):
        return text

    def return_buildings(self, request):
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