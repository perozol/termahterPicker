from __future__ import division
import re
import time
import json
import random
import math
from stemming import porter2
import operator

def tokenize(text):
    tokens = re.findall("[\w']+", text.lower())
    return [porter2.stem(token) for token in tokens]

class knn(object):
    def __init__(self):
        #self.docs is our training set
        self.docs = {}
        self.k = 16
        self.distances = {}
        
    def euclid(self, a, b):
        #a and b are vectors of actors
        #do euclidian distance between each two
        if len(a)== 0 and len(b) == 0:
            return 9999
        
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
    
    def most_common(self,lst):
        return max(set(lst), key=lst.count)
    
    def train(self, training):
        #training = dictionary of all vectorized movies
        
        for movie in training:
            
            self.docs[movie] = training[movie]
            rating = self.docs[movie]['rating']
            if rating == 10.0:
                self.docs[movie]['class'] = 10.0
            elif 10.0 > rating and rating >= 9.5:
                self.docs[movie]['class'] = 9.5
            elif 9.5 > rating and rating >= 9.0:
                self.docs[movie]['class'] = 9.0
            elif 9.0 > rating and rating >= 8.5:
                self.docs[movie]['class'] = 8.5
            elif 8.5 > rating and rating >= 8.0:
                self.docs[movie]['class'] = 8.0
            elif 8.0 > rating and rating >= 7.5:
                self.docs[movie]['class'] = 7.5
            elif 7.5 > rating and rating >= 7.0:
                self.docs[movie]['class'] = 7.0
            elif 7.0 > rating and rating >= 6.5:
                self.docs[movie]['class'] = 6.5
            elif 6.5 > rating and rating >= 6.0:
                self.docs[movie]['class'] = 6.0
            elif 6.0 > rating and rating >= 5.5:
                self.docs[movie]['class'] = 5.5
            elif 5.5 > rating and rating >= 5.0:
                self.docs[movie]['class'] = 5.0
            elif 5.0 > rating and rating >= 4.5:
                self.docs[movie]['class'] = 4.5
            elif 4.5 > rating and rating >= 4.0:
                self.docs[movie]['class'] = 4.0
            elif 4.0 > rating and rating >= 3.5:
                self.docs[movie]['class'] = 3.5
            elif 3.5 > rating and rating >= 3.0:
                self.docs[movie]['class'] = 3.0
            elif 3.0 > rating and rating >= 2.5:
                self.docs[movie]['class'] = 2.5
            elif 2.5 > rating and rating >= 2.0:
                self.docs[movie]['class'] = 2.0
            elif 2.0 > rating and rating >= 1.5:
                self.docs[movie]['class'] = 1.5
            elif 1.5 > rating and rating >= 1.0:
                self.docs[movie]['class'] = 1.0
            elif 1.0 > rating and rating >= 0.5:
                self.docs[movie]['class'] = 0.5
            else:
                self.docs[movie]['class'] = 0.0
            
    
    def classify(self, current, vspace):
        #current is the movie we want to classify against training set
        if vspace == 'plot':
            actorlist = current['plot']
        else:
            actorlist = current[vspace]
        
        
        dists = {}
        classes = {}
        sorted_dists = {}
        for movie in self.docs:
            templist = self.docs[movie][vspace]
            movie_class = self.docs[movie]['class']
            dist = self.euclid(actorlist, templist)
            dists[movie] = dist
            classes[movie] = movie_class
            
        sorted_dists = sorted(dists.iteritems(), key=operator.itemgetter(1))
        
        
        ids = []
        for x in range(0, self.k):
            ids.append(sorted_dists[x][0])
        """
        for id in ids:
            return ratings[id]
        """

        list = [classes[id] for id in ids]
            #print list
        common_categorie = self.most_common(list)

        return common_categorie
