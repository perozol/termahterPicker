from __future__ import division
import re
import math
import operator
import collections
import ujson
from stemming import porter2
from collections import Counter

def tokenize(text):
    tokens = re.findall("[\w']+", text.lower())
    return [porter2.stem(token) for token in tokens]

def read_movies(filename):
    file = open(filename)
    for line in file:
        yield ujson.loads(line)
    file.close()

class vector(object):

    def __init__(self, db):
        self.movie_vectors = dict()
        self.db = db
        self.total = 0

    def vectorize_plot(self,movie):
        """
            purpose: read the movie and turn it into a vector of
                plot phrases
            parameters:
            movies - a dictionary of a movie
            returns: none
        """
 
        if 'plot_simple' in movie:
            plot = tokenize(movie['plot_simple'])
            rating = movie['rating']
            ratingcount = movie['rating_count']
            plot_vector = dict()
            count = 0
            for word in plot:
                plot_vector[word] = len(word)/(((rating)*math.log(ratingcount,10))/math.log(self.total,15))
                count += 1

            return plot_vector
        else:
            return {}

    def vectorize_actor(self,movie):
        """
            purpose: read the movie and turn it into a vector of
                actors
            parameters:
                movies - a dictionary of a movie
            returns: none
        """

        if 'actors' in movie:
            actors = movie['actors']
            ratingcount = movie['rating_count']
            rating = movie['rating']
            actor_vector = dict()
            count = 0
            for actor in actors:
                alpha = math.exp(-ratingcount)
                actor_vector[actor] = ((rating)*math.log(ratingcount,10))/math.log(self.total,15)
                count += 1

            return actor_vector
        else:
            return {}

    def vectorize_writer(self,movie):
        """
            purpose: read the movie and turn it into a vector of
                writers
            parameters:
            movies - a dictionary of a movie
            returns: none
        """
 
        if 'writers' in movie:
            writers = movie['writers']
            rating = movie['rating']
            ratingcount = movie['rating_count']
            writers_vector = dict()
            count = 0
            for writer in writers:
                writers_vector[writer] = ((rating)*math.log(ratingcount,10))/math.log(self.total,15)
                count += 1

            return writers_vector
        else:
            return {}

    def vectorize_director(self,movie):
        """
            purpose: read the movie and turn it into a vector of
                directors
            parameters:
            movie - a dictionary of a movie
            returns: none
        """
        
        if 'directors' in movie:
            directors = movie['directors']
            ratingcount = movie['rating_count']
            rating = movie['rating']
            directors_vector = dict()
            count = 0
            for director in directors:
                directors_vector[director] = ((rating)*math.log(ratingcount,10))/math.log(self.total,15)
                count += 1
            
            return directors_vector
        else:
            return {}
    def vectorize_genre(self,movie):
        """
            purpose: read the movie and turn it into a vector of
                directors
            parameters:
            movie - a dictionary of a movie
            returns: none
        """
        
        if 'genres' in movie:
            genres = movie['genres']
            rating = movie['rating']
            genre_vector = dict()
            ratingcount = movie['rating_count']
            count = 0
            for genre in genres:
                genre_vector[genre] = ((rating)*math.log(ratingcount,10))/math.log(self.total,15)
                count += 1
            
            return genre_vector
        else:
            return {}


    def vectorize(self,movies, collection):

        """
            purpose: read the movies and turn them into vectors of
                actors, writers, directors, and plot
            parameters:
                movies - an iterator of movie dictionaries
            returns: none
        """
        movie_vectors = {}
        ratingmax = 0

        tempmovies = read_movies('mv.json')
        
        for movie in tempmovies:
            if 'rating_count' in movie:
                if movie['rating_count'] > ratingmax:
                    ratingmax = movie['rating_count']

        self.total = ratingmax
            
        for movie in movies:
            if 'imdb_id' and 'rating_count' in movie:
                movie_id = movie['imdb_id']
                movie_rating = -1.0
                if 'rating' in movie:
                    movie_rating = movie['rating']
                
                movie_dict = {}
                movie_dict['title'] = movie['title']
                movie_dict['actors'] = self.vectorize_actor(movie)
                movie_dict['writers'] = self.vectorize_writer(movie)
                movie_dict['directors'] = self.vectorize_director(movie)
                movie_dict['plot'] = self.vectorize_plot(movie)
                movie_dict['genres'] = self.vectorize_genre(movie)
                ratingcount = movie['rating_count']
                movie_dict['rating'] = movie['rating']
                #print 
                #print "OLD: ", movie_rating
                #movie_dict['rating'] = ((movie_rating)*math.log(ratingcount,10))/math.log(self.total,15)
                #print "RATINGC", ratingcount
                #print "NEW: " , movie_dict['rating']
                #print
                movie_dict['rating_count'] = movie['rating_count'] 
                
                #movie_dict['plot'] = self.vectorize_plot(movie)
                
                movie_vectors[movie_id] = movie_dict
                if collection == 'training':
                    d = dict(
                        info = movie,
                        imdb_id = movie_id
                    )
                    self.db[collection].insert(d)
    
        if collection == 'training':
            self.db[collection].create_index('imdb_id')

        return movie_vectors



