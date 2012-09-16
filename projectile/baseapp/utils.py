# -*- coding: utf-8 -*-

from django.db import connection, transaction
from django.contrib import messages

import urllib2
import re
import time

try:
    from projectapps.mail_e.utils import send_mail2 as send
except ImportError:
    send = ()
import page_messages_list as pml



#TODO : comment!
def send_mail(email_to, subject, content):
    return send(email_to, subject, content)



def db_query_dict(query):
    '''
    принимает query - SQL запрос
    выполняет запрос к базе и отдаёт ассоциативный массив
    имена полей в query должны быть либо уникальными либо именоваными
    '''

    cursor = connection.cursor()
    cursor.execute(query)

    desc = cursor.description

    q_list = list()

    for i in range(cursor.rowcount):
        q_dict = dict()
        data = cursor.fetchone()
        for name, value in zip(desc, data) :
            q_dict[name[0]] = value
        q_list.append(q_dict)

    return q_list, cursor.rowcount
#    return q_list



def page_message(request, code=None, text=None, type='ERROR'):
    message_text = ''

    if text:
        message_text = text
    else:
        if code == '':
            message_text = 'Blank'
        else:
            if code in pml.m_text:
                message_text = pml.m_text[code]
            elif code in pml.m_code :
                message_text = pml.m_code[code]

    if type == 'error':
        messages.add_message(request, messages.ERROR, message_text, fail_silently=True)
    elif type == 'info':
        messages.add_message(request, messages.INFO, message_text, fail_silently=True)
    elif type == 'success':
        messages.add_message(request, messages.SUCCESS, message_text, fail_silently=True)
    else:
        messages.add_message(request, messages.ERROR, message_text, fail_silently=True)



def render_me_price(r_string):
    '''
    форматирование цены
    '''
    string = r_string

    if type(r_string) == float:
        string = "%0.2f" % (r_string)
    elif type(r_string) == int:
        string = str(r_string)
    elif type(r_string) == str and len(r_string.split('.')) > 1:
        string = "%0.2f" % (float(r_string))

    if 'None' in str(type(r_string)):
        data = r_string
    else:
        data = ''

        if len(string.split('.')) > 1:
            str_int, str_dec = string.split('.')
        else:
            str_int = string

        for i in range(len(str_int)):
            str_int_revert = str_int[::-1]
            data += str_int_revert[len(str_int)-(len(str_int)-i)]
            z = str((float(i)+1)/3).split('.')
            if z[1] == '0':
                data += ' '
        data = data[::-1]

        try:
            data += '.%s' % str_dec
        except UnboundLocalError:
            pass

    return data






def send_sms(r_to, r_str):
    text = r_str.replace(' ', '%20')

    theurl = 'http://gate.sms-start.ru/send/'
    theurl2 = 'http://gate.sms-start.ru/send/?phone={phone}&text={text}&sender=STAKOS.RU'.format(
        phone = r_to,
        text = text
        )
    username = 'stakos'
    password = 's13s11'

    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, theurl, username, password)
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    pagehandle = urllib2.urlopen(theurl2)

#    print pagehandle.read()
    return pagehandle.read()

def sms_request_status(sms_id='57338207'):
    theurl = 'http://gate.sms-start.ru/status/'
    theurl2 = 'http://gate.sms-start.ru/status/?id={sms_id}'.format(
        sms_id = sms_id,
        )
    username = 'stakos'
    password = 's13s11'

    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, theurl, username, password)
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    pagehandle = urllib2.urlopen(theurl2)

#    print pagehandle.read()
    return pagehandle.read()




def phone_validate_util(function):
    '''
    декоратор создаёт сообщение если моб.номер не подтверждён
    '''
    def new(request, *args, **kwargs):
#        print request
        if not request.user.phone_mobile_status:
            page_message(request, 70, None, 'info')
        return function(request, *args, **kwargs)
    return new

def phone_formater(r_str):
    """
    форматирует телефон
    удаляет всё не цифровое
    отдаёт только 10 первых цифр
    """

    string = re.sub(r"\D", '', r_str)
    string = string.encode()
    if len(string) >= 10:
        string = string[-10:]
    return string




def timeit(method):
    """
    декоратор принтит время выполнния метода
    !!! не использовать в продакшене, или переписать принт !!!
    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r (%r) %2.2f sec' % (method.__name__, kw, te-ts)
        return result

    return timed


def cleanup_util(r_str):
    """
    очищает строку от всего лишнего
    нужно для поиска
    работает с кириллицей
    """
    return re.sub(ur'[^а-яa-z0-9]', u'', r_str.lower(), re.UNICODE)

def lang_stub(text=''):
    return text

