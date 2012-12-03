from __future__ import division
import knn
import time
import ujson
import utils
import vectorization


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
    print classify_movies
    classify_movies = vectorize.vectorize(classify_movies)
   
    
    # Execute classifier algorithm
    k.train(training_movies)
    
    for movie in classify_movies:
        actor_rating = k.classify(classify_movies[movie], 'actors')
        director_rating = k.classify(classify_movies[movie], 'directors')
        writer_rating = k.classify(classify_movies[movie], 'writers')
        plot_rating = k.classify(classify_movies[movie], 'plot')
        genre_rating = k.classify(classify_movies[movie], 'genre')
        
        avg = (actor_rating*.6) + (director_rating*.3) + (writer_rating*.05) + (genre_rating*.03) + (plot_rating*.03)
        
        print "Title: %s" % (classify_movies[movie]['title'])
        print "Actor rating: %f" % (actor_rating)
        print "Director rating: %f" % (director_rating)
        print "Writer rating: %f" % (writer_rating)
        print "Genre rating: %f" % (genre_rating)
        print "Plot rating: %f" % (plot_rating)
        print "----------------------"
        print "Final Rating: %f" %(avg)

if __name__=="__main__":
    start = time.time()
    main()
    print "Finished after %d seconds" % (time.time()-start)
    pass
