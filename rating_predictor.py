from __future__ import division
import knn
import time
import ujson
import upcomingReleases
import utils
import vectorization
import math
from pymongo import connection
from settings import settings

class Predictor():
    
    def __init__(self):
        self.predictions = []
        self.db = utils.connect_db('termather', remove_existing=True)

    def copy_dict(d):
        keys = d.keys()
        movie = {}
        for key in keys:
            movie[key] = d[keys]

        return movie

    def main(self):
        
        vectorize = vectorization.vector(self.db)
        k = knn.knn(self.db)
        
        # Read and vectorize movie data
        training_movies = utils.read_movies('mv.json')
        training_movies = vectorize.vectorize(training_movies, 'training')
        print "Training with %d movies" % len(training_movies)
        
        upcomingReleases.getUpcomingReleases()
        classify_movies = utils.read_movies('newReleases.json')
        c = {}
        print "#################################"
        print "Movies to classify"
        for movie in classify_movies:
            if 'imdb_id' in movie:
                movie['rating'] = 5.0
                movie['rating_count'] = 100
                c[movie['imdb_id']] = movie
                print "Title: %s" % movie['title']
        print "#################################"
        
        classify_movies_vectors = vectorize.vectorize(c.itervalues(), 'classified')

        # Execute classifier algorithm
        k.train(training_movies)
        errorsum = 0
        count = 0

        for movie in classify_movies_vectors:
            oldrating = classify_movies_vectors[movie]['rating']
            classify_movies_vectors[movie]['rating'] = k.avgrating
            actor_rating = k.classify(classify_movies_vectors[movie], 'actors')
            director_rating = k.classify(classify_movies_vectors[movie], 'directors')
            writer_rating = k.classify(classify_movies_vectors[movie], 'writers')
            plot_rating = k.classify(classify_movies_vectors[movie], 'plot')
            genre_rating = k.classify(classify_movies_vectors[movie], 'genres')
            count = count+1
            avg = (actor_rating*.14) + (director_rating*.2) + (plot_rating*.19) + (genre_rating*.28) + (writer_rating*.13)

            classify_movies_vectors[movie]['rating'] = avg
            c[movie]['rating'] = avg
            d = dict(
                  info = c[movie],
                  imdb_id = movie
                  )
            self.db['classified'].insert(d)
            self.predictions.append(d['info'])

            error = math.fabs((oldrating - avg)/oldrating)
            
            if error < 90:
                errorsum = errorsum + error
            title = classify_movies_vectors[movie]['title']

            """
            print count
            
            print
            print "Title: %s" % title
            print "Actor rating: %f" % (actor_rating)
            print "Director rating: %f" % (director_rating)
            print "Writer rating: %f" % (writer_rating)
            print "Genre rating: %f" % (genre_rating)
            print "Plot rating: %f" % (plot_rating)
            print "----------------------"
            print "Final Rating: %f" %(avg)
            print "Actual Rating: %f" %(oldrating)
            print "Error: %f" %(error*100)
            """
        
        self.db['classified'].create_index('imdb_id')
        
        """
        print "*************************************"
        print "AVERAGE ERROR: %f" %(100*errorsum/count)
        print "*************************************"
        """
