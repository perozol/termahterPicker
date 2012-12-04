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
    file = open('newReleases.json','w')
    for movie in upcoming:
        title = movie['title']
        query = 'q=' + title.replace(" ","+")
        r = requests.get(host+query+parameters)

        if ((r.json is not None) and (type(r.json) == dict)):
            # Write movie data
            data = StringIO()
            json.dump(r.json, data)
            file.write(data.getvalue())
            file.write(",\n")
    file.close()

if __name__=="__main__":
    start = time.time()
    print getUpcomingReleases()
    pass