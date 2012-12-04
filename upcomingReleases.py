import requests
import json
from StringIO import StringIO
import time
import re

def getUpcomingReleases():
    url = 'http://api.rottentomatoes.com/api/public/v1.0/lists/movies/upcoming.json?apikey=rnvv7jdrtzez73944vaxu74r'
    r = requests.get(url)

    host = 'http://imdbapi.org/?'
    parameters = '&type=json&lang=en-US'

    upcoming = r.json['movies']
    newReleases = []
    for movie in upcoming:
        title = movie['title']
        query = 'q=' + title.replace(" ","+")
        r = requests.get(host+query+parameters)

        if ((r.json is not None) and (type(r.json) == dict)):
            r.json['rating'] =  5.0
            newReleases.append(r.json)

    return newReleases

if __name__=="__main__":
    start = time.time()
    print getUpcomingReleases()
    pass