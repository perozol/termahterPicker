import knn
import time
import ujson
import utils
import vectorization

def read_training_movies():
    file = open('sample_training_corpus.json')
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
    
    for movie in classify_movies:
        rating = k.classify(classify_movies[movie])
        print "Title: %s" % (classify_movies[movie]['title'])
        print "Rating: %f" % (rating)

if __name__=="__main__":
    start = time.time()
    main()
    print "Finished after %d seconds" % (time.time()-start)
    pass