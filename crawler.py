import requests
import json
from StringIO import StringIO
import time
import re

movies = []

f = open('filmsOf2012.txt')
for line in f:
    s = line
    #list = s.split('::')
    name = s[:-1]
    year = ""
    """
    for x in range(len(s)-5,len(s)-1):
        year += s[x]
    name = name[:-8]
    """
    movie = {'name': s, 'year': year}
    movies.append(movie)
f.close()

file = open("movie_corpus12.json",'w')
statistics = open("stats12.txt",'w')

numOfMovies = 0
moviesPerYear = {}
start = time.time()
for movie in movies:
    
    host = 'http://imdbapi.org/?'
    query = 'q=' + movie['name'].replace(" ","+")
    print query
    parameters = '&type=json&lang=en-US'
    r = requests.get(host+query+parameters)

    if (r.json is not None):
        if (type(r.json) == list):
            print "Working"
            # Collect statistics
            numOfMovies += 1
            if (movie['year'] not in moviesPerYear):
                moviesPerYear[movie['year']] = 1
            else:
                moviesPerYear[movie['year']] += 1
                
            # Write movie data
            data = StringIO()
            json.dump(r.json[0], data)
            file.write(data.getvalue())
            file.write(",\n")
        if (type(r.json) == dict):
            print "Working"
            numOfMovies += 1
            if (movie['year'] not in moviesPerYear):
                moviesPerYear[movie['year']] = 1
            else:
                moviesPerYear[movie['year']] += 1
            
            # Write movie data
            data = StringIO()
            json.dump(r.json, data)
            file.write(data.getvalue())
            file.write(",\n")

end = time.time()
print "Finished in %d seconds" % (end-start)

# Write movie statistics
statistics.write("*** Statistics ***\n")
statistics.write("Number of movies: ")
statistics.write(str(numOfMovies) + "\n")
statistics.write("Distribution of movies over years: \n")
for year in moviesPerYear:
    statistics.write(year + ": " + str(moviesPerYear[year]) + "\n")

file.close()
statistics.close()
