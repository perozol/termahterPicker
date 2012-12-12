import operator
import re
from collections import defaultdict


from stemming import porter2


def tokenize(text):
    """
    Take a string and split it into tokens on word boundaries.

    A token is defined to be one or more alphanumeric characters,
    underscores, or apostrophes.  Remove all other punctuation, whitespace, and
    empty tokens.  Do case-folding to make everything lowercase. This function
    should return a list of the tokens in the input string.
    """
    tokens = re.findall("[\w']+", text.lower())
    return [porter2.stem(token) for token in tokens]


class MovieSearch(object):
    """ A search engine for movies. """
    def __init__(self, mongo):
        """
        purpose: Create the search engine for movies
        parameters:
            mongo - the pymongo Database object
        """
        self.search_collection = mongo['search']

    def index_movies(self,movies):
        """
        purpose: read the movie dicts and store them in the database
        preconditions: the database is empty
        parameters:
          movies - an iterator of movie dictionaries
        returns: none
        """

        for movie in movies:
            # we make a set of the tokens to remove duplicates
            tokens = list(set(tokenize(movie['title'])))
            movie['tags'] = tokens
            self.search_collection.save(movie)
            self.search_collection.ensure_index('tags')
            

    def search_results(self, query):
        """
        purpose: searches for the terms in "query" in our corpus using logical
            AND. Put another way, it returns a list of all of the movies that
            contain all of the terms in query.
        preconditions: index_movies() has already processed the corpus
        parameters:
          query - a string of terms
        returns: list of dictionaries containing the movies
        """
        tokens = tokenize(query)
        movies = []
        counter = 0
        if tokens:
            results = self.search_collection.find({'$and': [{'tags': token} for token in tokens]}, {'_id': 0})
            for movie in results:
                if (counter < 100):
                    movies.append(movie)
                    counter += 1
                else:
                    break
                
        return movies
