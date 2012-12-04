from __future__ import division
import knn
import time
import ujson
import utils
import vectorization
import math


def read_training_movies():
    file = open('mv.json')
    for line in file:
        yield ujson.loads(line)
    file.close()

def main():

    vectorize = vectorization.vector()
    k = knn.knn()
    
    # Read and vectorize movie data
    training_movies = read_training_movies()
    training_movies = vectorize.vectorize(training_movies)

            
    
    classify_movies = utils.read_movies()
    classify_movies = vectorize.vectorize(classify_movies)
    
    
    # Execute classifier algorithm
    k.train(training_movies)
    errorsum = 0
    count = 0
    for movie in classify_movies:
        oldrating = classify_movies[movie]['rating']
        classify_movies[movie]['rating'] = k.avgrating
        actor_rating = k.classify(classify_movies[movie], 'actors')
        director_rating = k.classify(classify_movies[movie], 'directors')
        writer_rating = k.classify(classify_movies[movie], 'writers')
        plot_rating = k.classify(classify_movies[movie], 'plot')
        genre_rating = k.classify(classify_movies[movie], 'genres')
        count = count+1
        avg = (actor_rating*.5) + (director_rating*.3) + (plot_rating*.1) + (genre_rating*.1)
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
        
    print "*************************************"
    print "AVERAGE ERROR: %f" %(100*errorsum/count)
    print "*************************************"
if __name__=="__main__":
    start = time.time()
    main()
    print "Finished after %d seconds" % (time.time()-start)
    pass
