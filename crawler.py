import requests
import json
from StringIO import StringIO
import time
import re

movies = []

f = open('movies.txt', 'r')

for line in f:
    s = line
    list = s.split('::')
    name = list[1]
    year = ""
    for x in range(len(list[1])-5,len(list[1])-1):
        year += list[1][x]
    name = name[:-7]

    movie = {'name': name, 'year': year}
    movies.append(movie)
f.close()

file = open("movie_corpus.json",'w')
statistics = open("stats.txt",'w')

numOfMovies = 0
moviesPerYear = {}
start = time.time()
for movie in movies[:10]:
    
    host = 'http://imdbapi.org/?'
    query = 'q=' + movie['name'].replace(" ","+")
    parameters = '&type=json&lang=en-US'
    r = requests.get(host+query+parameters)
    
    if (r.json is not None):
        if (type(r.json) == type(list)):
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