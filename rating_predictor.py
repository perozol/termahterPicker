from __future__ import division
import knn
import time
import ujson
import upcomingReleases
import utils
import vectorization
import math
import operator
from pymongo import connection
from settings import settings

class Predictor():
    
    def __init__(self, db):
        self.k = knn.knn()
        self.training = db['training']
        self.classified = db['classified']
        self.gold = db['gold']
        self.golden = {}
    
    def train_classifier(self, training_movies):
        vectorize = vectorization.vector()
        
        # Vectorize movie data and traing classifier
        training_movies = vectorize.vectorize(training_movies, self.training, 'training')
        self.training.create_index('imdb_id')
        print "Training with %d movies" % len(training_movies)
    
        self.k.train(training_movies)
    
    def golden_movie(self):
    
        actor_scores = sorted(self.k.actor_avg.iteritems(), key=operator.itemgetter(1))
        actor_scores.reverse()
        director_scores = sorted(self.k.dir_avg.iteritems(), key=operator.itemgetter(1))
        director_scores.reverse()
        genre_score = sorted(self.k.gen_avg.iteritems(), key=operator.itemgetter(1))
        genre_score.reverse()
        
        self.golden = dict(
                           imdb_id = '0',
                           rating = '5.5',
                           rating_count = '100',
                           title = 'The Greatest Movie Never Made',
                           year = '2020',
                           actors = [x[0] for x in actor_scores[:3]],
                           directors = [director_scores[0][0]],
                           genre = genre_score[0][0],
                           poster = '/static/images/caverlee.png')
        """
        vectorize = vectorization.vector()
        classify = vectorize.vectorize([self.golden],self.gold,'golden')
    
        actor_rating = self.k.classify(self.golden, 'actors')
        director_rating = self.k.classify(self.golden, 'directors')
        genre_rating = self.k.classify(self.golden, 'genres')
    
        avg = (actor_rating*.14) + (director_rating*.2) + (genre_rating*.28)
        self.golden['rating'] = avg
        """
        return self.golden

    def main(self, movies):
        
        vectorize = vectorization.vector()

        classify_movies = {}
        print "#################################"
        print "Movies to classify"
        for movie in movies:
            classify_movies[movie['imdb_id']] = movie
            print "Title: %s" % movie['title']
        print "#################################"
        
        classify_movies_vectors = vectorize.vectorize(classify_movies.itervalues(), self.classified, 'classified')

        # Execute classifier algorithm

        errorsum = 0
        count = 0

        for movie in classify_movies_vectors:
            oldrating = classify_movies_vectors[movie]['rating']
            classify_movies_vectors[movie]['rating'] = self.k.avgrating
            actor_rating = self.k.classify(classify_movies_vectors[movie], 'actors')
            director_rating = self.k.classify(classify_movies_vectors[movie], 'directors')
            writer_rating = self.k.classify(classify_movies_vectors[movie], 'writers')
            plot_rating = self.k.classify(classify_movies_vectors[movie], 'plot')
            genre_rating = self.k.classify(classify_movies_vectors[movie], 'genres')
            count = count+1
            avg = (actor_rating*.14) + (director_rating*.2) + (plot_rating*.19) + (genre_rating*.28) + (writer_rating*.13)

            classify_movies_vectors[movie]['rating'] = avg
            classify_movies[movie]['rating'] = avg

            self.classified.insert(classify_movies[movie])

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
        
        self.classified.create_index('imdb_id')
        
        """
        print "*************************************"
        print "AVERAGE ERROR: %f" %(100*errorsum/count)
        print "*************************************"
        """
