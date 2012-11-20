import re
import math
import operator
import collections
from stemming import porter2
from collections import Counter

class vector(object):

    def __init__(self):
        self.movie_vectors = dict()

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
            rating = movie['rating']
            
            actor_vector = dict()
            count = 0
            alpha = float(len(actors))/100.0
            alpha = rating*alpha
            for actor in actors:
                actor_vector[actor] = alpha*math.exp(-alpha*count)
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

            writers_vector = dict()
            count = 0
            alpha = float(len(writers))/100.0
            for writer in writers:
                writers_vector[writer] = alpha*math.exp(-alpha*count)
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
            
            directors_vector = dict()
            count = 0
            alpha = float(len(directors))/100.0
            for director in directors:
                directors_vector[director] = alpha*math.exp(-alpha*count)
                count += 1
            
            return directors_vector
        else:
            return {}

    def vectorize(self,movies):

        """
            purpose: read the movies and turn them into vectors of
                actors, writers, directors, and plot
            parameters:
                movies - an iterator of movie dictionaries
            returns: none
        """
        movie_vectors = dict()
        
        for movie in movies:
            movie_id = movie['imdb_id']
            movie_rating = -1.0
            if 'rating' in movie:
                movie_rating = movie['rating']
            
            movie_dict = dict()
            movie_dict['title'] = movie['title']
            movie_dict['actors'] = self.vectorize_actor(movie)
            movie_dict['writers'] = self.vectorize_writer(movie)
            movie_dict['directors'] = self.vectorize_director(movie)
            movie_dict['rating'] = movie_rating
            #movie_dict['plot'] = self.vectorize_plot(movie)

            movie_vectors[movie_id] = movie_dict

        return movie_vectors



