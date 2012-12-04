import re
import math
import operator
import collections
from stemming import porter2
from collections import Counter

def tokenize(text):
    tokens = re.findall("[\w']+", text.lower())
    return [porter2.stem(token) for token in tokens]

class vector(object):

    def __init__(self, db):
        self.movie_vectors = dict()
        self.db = db

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
            plot_vector = dict()
            count = 0
            for word in plot:
                plot_vector[word] = len(word)/rating
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
            
            rating = movie['rating']
            actor_vector = dict()
            count = 0
            for actor in actors:
                actor_vector[actor] = rating
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
            writers_vector = dict()
            count = 0
            for writer in writers:
                writers_vector[writer] = rating
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
            rating = movie['rating']
            directors_vector = dict()
            count = 0
            for director in directors:
                directors_vector[director] = rating
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
            count = 0
            for genre in genres:
                genre_vector[genre] = rating
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
        
        for movie in movies:
            if 'imdb_id' in movie:
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
                movie_dict['rating'] = movie_rating
                
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



