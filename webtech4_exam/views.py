# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render
import redis
from django.views.decorators.csrf import csrf_exempt

r_db = redis.StrictRedis(host='localhost', port=6379, db=0)


# Create your views here.

def index(request):
    result = r_db.hgetall('movies')
    output = '<body>'
    for item in result:
        output += '<p>Movie: ' + item + '<br />Actors: ' + r_db.hget('movies', item) + '</p>'
    output += '</body>'
    return HttpResponse(output)


@csrf_exempt
def post(request):
    movie_name = request.GET.get('movie')
    actors = request.GET.get('actors')
    if movie_name is None:
        movie_name = request.POST.get('movie')
        actors = request.POST.get('actors')
    if movie_name is None or actors is None:
        return HttpResponseBadRequest('<body>'
                                      '<h1>Missing parameter(s)!</h1>'
                                      '<p>Requires request parameter \'movie\' and \'actors\''
                                      '</body>', )
    r_db.hset('movies', movie_name, actors)
    return HttpResponse('<body><h1>added!</h1></body>')


def init(request):
    r_db.hset('movies', 'The Godfather', 'Al Pacino, Marlon Brando, Robert Duvall')
    r_db.hset('movies', 'Schindler\'s List', 'Liam Neeson, Ralph Fiennes, Ben Kingsley')
    r_db.hset('movies', 'Saving Private', 'Ryan Tom Hanks, Matt Damon, Vin Diesel')
    r_db.hset('movies', 'Back to the Future', 'Michael J. Fox, Christopher Lloyd, Lea Thompson')
    r_db.hset('movies', 'Casablanca', 'Ingrid Bergman, Humphrey Bogart, Peter Lorre')
    r_db.hset('movies', 'The Big Lebowski', 'Julianne Moore, Jeff Bridges, Tara Reid')
    return HttpResponse('<body><h1>Default values added!</h1></body>')


@csrf_exempt
def search(request):
    if request.method == 'POST':
        movie = request.POST.get("movie")
        movie_actors = r_db.hget('movies', movie)
        if not movie_actors:
            return HttpResponseNotFound('<body><p>Movie not known</p</body>')
        return HttpResponse('<body>'
                            '<p>'
                            'movie: ' + movie + '<br />'
                                                'actors: ' + movie_actors +
                            '</p>'
                            '</body>')
    else:
        return HttpResponseBadRequest('POST REQUEST EXPECTED')
