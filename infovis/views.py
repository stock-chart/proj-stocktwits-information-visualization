from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from django.core.urlresolvers import reverse
from django.views import generic

from .models import *

import time
from datetime import datetime, timedelta
import random
import requests
import json

class IndexView(generic.ListView):
    template_name = 'infovis/index.html'

    def get_queryset(self):
    	return

def test(request):
	url = 'https://api.stocktwits.com/api/2/streams/all.json?access_token=ea054bba1e92787abc7d51b4a9bc3512eaa02599'
	response = requests.get(url=url)
	return HttpResponse(response)

def reset_database(request):
    print 'Initializing database...'
    # Reset database
    Message.objects.all().delete()
    Symbol.objects.all().delete()
    User.objects.all().delete()
    json_file = '/Users/YuandaLi/Programs/ST_Data_Parser/part_data_5K.json'
    # json_file = '/Users/YuandaLi/Programs/ST_Data_Parser/new_5K.json'
    cnt = 0
    for line in open(json_file):
        message_json = json.loads(line)
        # Parse message_json
        if 'symbols' in message_json:
            for symbol in message_json['symbols']:
                # print message_json['id'], symbol['symbol']
                message = Message(message_id=message_json['id'], body=message_json['body'], created_at=message_json['created_at'],
                            user_id=message_json['user']['id'], symbol_id=symbol['id'], sentiment='sentiment')
                #===============
                if (random.getrandbits(1) == 0):
                    message.sentiment='bull'
                else:
                    message.sentiment='bear'
                #===============
                message.save()
                # parse symbol
                if (len(Symbol.objects.filter(symbol_id=symbol['id'])) == 0):
                    new_symbol = Symbol(symbol_id=symbol['id'], symbol=symbol['symbol'], title=symbol['title'],
                                        exchange=symbol['exchange'], sector=symbol['sector'], industry=symbol['industry'],
                                        trending=symbol['trending'])
                    new_symbol.save()
                else:
                    # Existing symbol. Increase count
                    existing_symbol = Symbol.objects.get(symbol_id=symbol['id'])
                    existing_symbol.count += 1
                    existing_symbol.save()

        else:
            # No symbol message in message
            message = Message(message_id=message_json['id'], body=message_json['body'], created_at=message_json['created_at'],
                            user_id=message_json['user']['id'], symbol_id=-1, sentiment='sentiment')
            #===============
            if (random.getrandbits(1) == 0):
                message.sentiment='bull'
            else:
                message.sentiment='bear'
            #===============
            message.save()
        # Parse user
        if (len(User.objects.filter(user_id=message_json['user']['id'])) == 0):
            new_user = User(user_id=message_json['user']['id'], username=message_json['user']['username'], name=message_json['user']['name'])
            new_user.save()
        else:
            pass

        cnt += 1
        print cnt, 'Message', message_json['id'], 'created.'
    return HttpResponse('<h1>Database reset.</h1>')

def get_top_symbols(request):
    number = 50
    symbol_list = Symbol.objects.all().order_by("-count")[:number]
    result = []
    for symbol in symbol_list:
        symbol_item = {"id":symbol.symbol_id, "symbol":symbol.symbol,
                        "title":symbol.title, "sector":symbol.sector, "count":symbol.count}
        result.append(symbol_item)
    ret = json.dumps(result)
    return HttpResponse(ret)

def get_treemap(request):
    sector_list = Symbol.objects.values_list('sector').distinct()
    children_list = []
    for each_sector in sector_list:
        sector = each_sector[0]
        symbol_list = Symbol.objects.all().filter(sector=sector)
        sector_children = []
        for symbol in symbol_list:
            symbol_item = {"id":symbol.symbol_id, "title:": symbol.title, "count:": symbol.count, "sentiment": symbol.bull}
            sector_children.append(symbol_item)
        children_list.append({"name":sector, "children":sector_children})
    ret = json.dumps({"name":"treemap", "children":children_list})
    return HttpResponse(ret)

def get_latest_messages(request):
    number = 30
    message_list = Message.objects.all().order_by('-created_at').values('message_id', 'body', 'created_at', 'user_id', 'sentiment')[:30]
    result = []
    for msg in message_list:
        msg_user = User.objects.filter(user_id=msg['user_id']).values('username')[0]
        msg_item = {'message_id':msg['message_id'], 'body':msg['body'], 'created_at':str(msg['created_at']),
                    'user_id':msg['user_id'], 'username':msg_user['username'],
                    'sentiment': msg['sentiment']}
        result.append(msg_item)
    ret = json.dumps(result)
    return HttpResponse(ret)

def get_keyword_cloud(request):
    msg_list = Message.objects.all().values('body').distinct()
    ret = ''
    for msg in msg_list:
        ret += msg['body']
        ret += ' '
    return HttpResponse(ret)

def get_chart_data(request):
    period = 1800   # Each period is 1 second
    num = 24 * 3600 / period    # The charts shows data within 24 hours
    end_time = datetime(2010,1,5)
    start_time = end_time - timedelta(seconds=(3600 * 24))
    all_res = Message.objects.filter(created_at__range=[start_time, end_time])
    result = []
    for i in range(0, num):
        start = start_time + timedelta(seconds=i * period)
        end = start_time + timedelta(seconds=(i+1)*period)
        res = all_res.filter(created_at__range=[start, end])
        item = {"time_period":i, "start_time":str(start), "end_time":str(end),
                "volume":len(res), "sentiment":random.randint(20, 95)}
        result.append(item)
    ret = json.dumps(result)
    return HttpResponse(ret)
