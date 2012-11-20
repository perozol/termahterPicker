from __future__ import division
import re
import time
import json
import random
import math
from stemming import porter2
import operator



class knn(object):
    def __init__(self):
        #self.docs is our training set
        self.docs = {}
        self.k = 1
        self.distances = {}
        
    def euclid(self, a, b):
        #a and b are vectors of actors
        #do euclidian distance between each two
        if len(a)== 0 and len(b) == 0:
            return 0
        
        total = 0
        actors = []
        
        for actor in a:
            actors.append(actor)
        for actor in b:
            actors.append(actor)
        
        actors = list(set(actors))
        for actor in actors:
            if actor in a:
                x = a[actor]
            else:
                x = 0
            if actor in b:
                y = b[actor]
            else:
                y = 0
            total = total + math.pow((x - y),2)
            
        
        return math.sqrt(total)
    
    
    def classify(self, training, current):
        #training = dictionary of all vectorized movies
        #current is the movie we want to classify against training set
        self.docs = training
        actorlist = current['actors']
        
        dists = {}
        ratings = {}
        for movie in self.docs:
            templist = self.docs[movie]['actors']
            rating = self.docs[movie]['rating']
            self.euclid(actorlist, templist)
            dists[movie] = self.euclid(actorlist, templist)
            ratings[movie] = rating
            print dists[movie]
            print movie
            
        sorted_dists = sorted(dists.iteritems(), key=operator.itemgetter(1))

        ids = []
        for x in range(0, self.k):
            ids.append(sorted_dists[x][0])
            
        for id in ids:
            return ratings[id]
        
            

def main():
    docs = {}
    docs['001'] = {'rating': 9.0, 'actors':{'Christian Bale': 0.87, 'Jack Nicholson': 0.76}} 
    docs['002'] = {'rating': 8.7, 'actors':{'Dora The Explorer': 0.92, 'Jack Nicholson': 0.51}}
    docs['003'] = {'rating': 5.5, 'actors':{'Brad Pitt': 0.92, 'Mohamed Sleem': 0.91}}
    docs['004'] = {'rating': 8.8, 'actors':{'Bradley Cooper': 0.882, 'Dora The Explorer': 0.43}}

    x = {}
    x['actors'] = {'Dora The Explorer': 0.97, 'Bradley Cooper': 0.16}
    
    k = knn()
    print k.classify(docs, x)
    
if __name__=="__main__":
    main()
    print "done"
    pass
