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


def read_training_movies():
    file = open('mv.json')
    for line in file:
        yield ujson.loads(line)
    file.close()

def connect_db(dbname, remove_existing=False):
    con = connection.Connection(settings['mongo_host'],settings['mongo_port'])
    if remove_existing:
        con.drop_database(dbname)
    return con[dbname]

def main():
    
    db = connect_db('termather', remove_existing=True)
    
    vectorize = vectorization.vector(db)
    k = knn.knn(db)
    
    # Read and vectorize movie data
    training_movies = read_training_movies()
    training_movies = vectorize.vectorize(training_movies)

            
    
    #classify_movies = upcomingReleases.getUpcomingReleases()
    classify_movies = utils.read_movies()
    classify_movies_vectors = vectorize.vectorize(iter(classify_movies))
    
    
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
        avg = (actor_rating*.5) + (director_rating*.3) + (plot_rating*.1) + (genre_rating*.1)

        movie['rating'] = avg
        db['classified'].insert(movie)

        error = math.fabs((oldrating - avg)/oldrating)
        errorsum = errorsum + error
        
        """
        print "Title: ",  (classify_movies[movie]['title'])
        print "Actor rating: %f" % (actor_rating)
        print "Director rating: %f" % (director_rating)
        print "Writer rating: %f" % (writer_rating)
        print "Genre rating: %f" % (genre_rating)
        print "Plot rating: %f" % (plot_rating)
        print "----------------------"
        print "Final Rating: %f" %(avg)
        print "Actual Rating: %f" %(oldrating)
        print "Error: %f" %(error*100)"""
    
    db['classified'].create_index('imdb_id')
    print "*************************************"
    print "AVERAGE ERROR: %f" %(100*errorsum/count)
    print "*************************************"

    return db

if __name__=="__main__":
    start = time.time()
    main()
    print db['training'].find({'imdb_id': "tt0209475"})
    print db['classified'].find({'imdb_id': "tt0112573"})
    print "Finished after %d seconds" % (time.time()-start)
    pass
