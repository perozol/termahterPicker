#!/usr/bin/env python
# web server for tweet search
# You should not need to edit this file.

import time

import bottle
import rating_predictor as predictor
import ujson
from settings import settings

_predictor = None
imdb_id = 0

def read_movies(filename):
    file = open(filename)
    for line in file:
        yield ujson.loads(line)
    file.close()

@bottle.route('/search')
def search(name='World'):
    
    results = []

    for i in _predictor.predictions:
        if "poster" not in i:
            i['poster'] = '/static/images/caverlee.png'
        if "plot_simple" not in i:
            i['plot_simple'] = ''
        print i['title']
        results.append(i)
    
    return dict(
            movie = results,
            author = settings['author'],
            agree_to_honor_code = settings['agree_to_honor_code'],
            count = len(_predictor.predictions)
            )

@bottle.route('/get')
def info():
    movies = read_movies('test.json')
    
    result = {}
    start_time = time.time()
    global imdb_id
    for movie in movies:
        if movie['imdb_id'] == imdb_id:
            result = movie
    end_time = time.time()

    print result

    return dict(
            movie = result,
            author = settings['author'],
            agree_to_honor_code = settings['agree_to_honor_code'],
            time = end_time - start_time,
            )

@bottle.route('/static/info.html', method='POST')
def movie_info():
    global imdb_id
    imdb_id = bottle.request.forms.get('id')
    print imdb_id
    return bottle.static_file('info.html', root='static')

@bottle.route('/')
def index():
    return bottle.static_file('main.html', root='static')


@bottle.route('/favicon.ico')
def favicon():
    return bottle.static_file('favicon.ico', root='static')


@bottle.route('/static/<filename:path>')
def server_static(filename):
    return bottle.static_file(filename, root='static')


if __name__=="__main__":
    print "In Main"
    _predictor = predictor.Predictor()
    _predictor.main()
    bottle.run(host=settings['http_host'],
               port=settings['http_port'],
               reloader=True)
