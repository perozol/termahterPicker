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
        self.plot_avg = {}
        self.gen_avg = {}
        self.wri_avg = {}
        self.dir_avg = {}
        self.actor_avg = {}
        
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
                

        actor_avg = {}      
        for movie in training:
            actors = training[movie]['actors']
            for actor in actors:
                if actor not in actor_avg:
                    actor_avg[actor] = {}
                    actor_avg[actor]['count'] = 1
                    actor_avg[actor]['sum'] = actors[actor]
                    actor_avg[actor]['avg'] = actor_avg[actor]['sum']/actor_avg[actor]['count']
                    
                else:
                     actor_avg[actor]['count'] = actor_avg[actor]['count'] + 1
                     actor_avg[actor]['sum'] = actor_avg[actor]['sum'] + actors[actor] 
                     actor_avg[actor]['avg'] = actor_avg[actor]['sum']/actor_avg[actor]['count']
        dir_avg = {}     
        for movie in training:
            actors = training[movie]['directors']
            for actor in actors:
                if actor not in actor_avg:
                    dir_avg[actor] = {}
                    dir_avg[actor]['count'] = 1
                    dir_avg[actor]['sum'] = actors[actor]
                    dir_avg[actor]['avg'] = dir_avg[actor]['sum']/dir_avg[actor]['count']
                    
                else:
                     dir_avg[actor]['count'] = dir_avg[actor]['count'] + 1
                     dir_avg[actor]['sum'] = dir_avg[actor]['sum'] + actors[actor] 
                     dir_avg[actor]['avg'] = dir_avg[actor]['sum']/dir_avg[actor]['count']
        wri_avg = {}     
        for movie in training:
            actors = training[movie]['writers']
            for actor in actors:
                if actor not in actor_avg:
                    wri_avg[actor] = {}
                    wri_avg[actor]['count'] = 1
                    wri_avg[actor]['sum'] = actors[actor]
                    wri_avg[actor]['avg'] = wri_avg[actor]['sum']/wri_avg[actor]['count']
                    
                else:
                     wri_avg[actor]['count'] = wri_avg[actor]['count'] + 1
                     wri_avg[actor]['sum'] = wri_avg[actor]['sum'] + actors[actor] 
                     wri_avg[actor]['avg'] = wri_avg[actor]['sum']/wri_avg[actor]['count']
                     
        gen_avg = {}     
        for movie in training:
            actors = training[movie]['genres']
            for actor in actors:
                if actor not in actor_avg:
                    gen_avg[actor] = {}
                    gen_avg[actor]['count'] = 1
                    gen_avg[actor]['sum'] = actors[actor]
                    gen_avg[actor]['avg'] = gen_avg[actor]['sum']/gen_avg[actor]['count']
                    
                else:
                     gen_avg[actor]['count'] = gen_avg[actor]['count'] + 1
                     gen_avg[actor]['sum'] = gen_avg[actor]['sum'] + actors[actor] 
                     gen_avg[actor]['avg'] = gen_avg[actor]['sum']/gen_avg[actor]['count']
                     
        plot_avg = {}     
        for movie in training:
            actors = training[movie]['plot']
            for actor in actors:
                if actor not in actor_avg:
                    plot_avg[actor] = {}
                    plot_avg[actor]['count'] = 1
                    plot_avg[actor]['sum'] = plot_avg[actor]
                    plot_avg[actor]['avg'] = plot_avg[actor]['sum']/plot_avg[actor]['count']
                    
                else:
                     plot_avg[actor]['count'] = plot_avg[actor]['count'] + 1
                     plot_avg[actor]['sum'] = plot_avg[actor]['sum'] + actors[actor] 
                     plot_avg[actor]['avg'] = plot_avg[actor]['sum']/plot_avg[actor]['count']

        self.plot_avg = plot_avg
        self.gen_avg = gen_avg
        self.wri_avg = wri_avg
        self.dir_avg = dir_avg
        self.actor_avg = actor_avg
                
    
    def classify(self, current, vspace):
        #current is the movie we want to classify against training set

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
