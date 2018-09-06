# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
import redis

r_db = redis.StrictRedis(host='localhost', port=6379, db=0)


# Create your views here.

def index(request):
    result = r_db.hgetall('movies')
    output = '<body>'
    for item in result:
        output += '<p>Movie: ' + item + '<br />Actors: ' + r_db.hget('movies', item) + '</p>'
    output += '</body>'
    return HttpResponse(output)

