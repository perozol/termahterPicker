import json
import time
import utils
import csv

movies = utils.read_tweets()

numOfMovies = 0
years = {}
actor_information = {}
director_information = {}

for movie in movies:
    
    numOfMovies += 1
    
    if 'year' in movie:
        year = movie['year']
    
    if 'actors' in movie:
        actors = movie['actors']
    
    if 'directors' in movie:
        directors = movie['directors']

    if year in years:
        years[year] += 1
    else:
        years[year] = 1

    for actor in actors:
        if actor in actor_information:
            actor_information[actor]['movies'] += 1
        else:
            dict = {'movies': 1}
            actor_information[actor] = dict

    for director in directors:
        if director in director_information:
            director_information[director]['movies'] += 1
        else:
            dict = {'movies': 1}
            director_information[actor] = dict

file = open('number_of_movies.txt', 'w')
file1 = open('year_statistics.csv', 'wb')
file2 = open('actor_statistics.csv', 'wb')

string = 'Number of Movies: %d' % numOfMovies
file.write(string)
file.close()

file1.write('Year, Number of Movies\n')
file2.write('Actor, Number of Movies\n')

for key, value in years.items():
    string = '%s, %d\n' % (key,value)
    file1.write(string.encode('utf8'))

for key in actor_information:
    string = '%s, %d\n' % (key,actor_information[key]['movies'])
    file2.write(string.encode('utf8'))

file1.close()
file2.close()
