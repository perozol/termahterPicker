#!/usr/bin/env python
# web server for tweet search
# You should not need to edit this file.

import bottle
import json
import moviesearch
import rating_predictor as predictor
from settings import settings
from StringIO import StringIO
import time
import upcomingReleases
import utils

_predictor = None
_searcher = None
_db = None
imdb_id = 0
query = 0

@bottle.route('/predict')
def predict(name='World'):
    
    movies = []
    cursor = _db['classified'].find({},{'_id': 0}).sort(u'rating', -1)
    for movie in cursor:
        if "poster" not in movie:
            movie['poster'] = '/static/images/caverlee.png'
        if "plot_simple" not in movie:
            movie['plot_simple'] = ''
        movies.append(movie)
    
    return dict(
            movies = movies,
            author = settings['author'],
            agree_to_honor_code = settings['agree_to_honor_code'],
            count = len(movies)
            )

@bottle.route('/get')
def search():
    global _searcher
    query = bottle.request.query.q
    start_time = time.time()
    movies = _searcher.search_results(query)
    end_time = time.time()

    return dict(
                movies = movies,
                author = settings['author'],
                agree_to_honor_code = settings['agree_to_honor_code'],
                count = len(movies),
                time = end_time - start_time,
                )

@bottle.route('/fill')
def golden_movie_info():
    movie = _predictor.golden_movie()

    return dict( movies= [movie])

@bottle.route('/golden')
def golden_movie():
    return bottle.static_file('golden.html', root='static')

@bottle.route('/search')
def movie_info():
    return bottle.static_file('search.html', root='static')

@bottle.route('/')
def index():
    return bottle.static_file('main.html', root='static')


@bottle.route('/favicon.ico')
def favicon():
    return bottle.static_file('favicon.ico', root='static')


@bottle.route('/static/<filename:path>')
def server_static(filename):
    return bottle.static_file(filename, root='static')

def init(db):
    upcomingReleases.getUpcomingReleases()
    
    iter = utils.read_movies('newReleases.json')
    collection = []
    
    print "Pre-processing data"
    start = time.time()
    # Pre-process movies to classify
    file = open('classify.json','w')
    for movie in iter:
        if 'imdb_id' in movie:
            movie['rating'] = 5.0
            movie['rating_count'] = 100
            collection.append(movie)
            
            # Write movie data
            data = StringIO()
            json.dump(movie, data)
            file.write(data.getvalue())
            file.write(",\n")
    file.close()
    end = time.time()
    print "Finished in %.3f seconds\n" % (end-start)
    
    iter = utils.read_movies('mv.json')
    for movie in iter:
        collection.append(movie)

    for movie in collection:
        if "poster" not in movie:
            movie['poster'] = '/static/images/caverlee.png'
        if "plot_simple" not in movie:
            movie['plot_simple'] = ' '
        if "director" not in movie:
            movie['directors'] = ['Unknown']

    print "Indexing movie titles"
    start = time.time()
    indexer = moviesearch.MovieSearch(db)
    indexer.index_movies(collection)
    end = time.time()
    print "Finished in %.3f seconds\n" % (end-start)


if __name__=="__main__":
    print "In Main"
    _db = utils.connect_db('termather',remove_existing=True)
    init(_db)
    _predictor = predictor.Predictor(_db)
    _predictor.train_classifier(utils.read_movies('mv.json'))
    _predictor.main(utils.read_movies('classify.json'))
    _searcher = moviesearch.MovieSearch(_db)
    
    bottle.run(host=settings['http_host'],
               port=settings['http_port'])
