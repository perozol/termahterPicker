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
        self.k = 11
        self.distances = {}
        self.plot_avg = {}
        self.gen_avg = {}
        self.wri_avg = {}
        self.dir_avg = {}
        self.actor_avg = {}
        self.avgrating = 0
    
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


        ratingmax = 0
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
        dir_avg = {}
        wri_avg = {}
        gen_avg = {}
        plot_avg = {}
        rating_sum = 0
        rcount = 0
       
        countsum = 0

        rmax = 0
        
        for movie in training:
            actors = training[movie]['actors']
            rcount = rcount + 1
            rating_sum = rating_sum + training[movie]['rating']
            countsum = countsum + training[movie]['rating_count']
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
                     
            directors = training[movie]['directors']
            for director in directors:
                if director not in dir_avg:
                    dir_avg[director] = {}
                    dir_avg[director]['count'] = 1
                    dir_avg[director]['sum'] = directors[director]
                    a = dir_avg[director]['sum']
                    b = dir_avg[director]['count']
                    dir_avg[director]['avg'] = a/b
                    
                else:
                     dir_avg[director]['count'] = dir_avg[director]['count'] + 1
                     dir_avg[director]['sum'] = dir_avg[director]['sum'] + directors[director] 
                     dir_avg[director]['avg'] = dir_avg[director]['sum']/dir_avg[director]['count']

            writers = training[movie]['writers']
            for writer in writers:
                if writer not in wri_avg:
                    wri_avg[writer] = {}
                    wri_avg[writer]['count'] = 1
                    wri_avg[writer]['sum'] = writers[writer]
                    wri_avg[writer]['avg'] = wri_avg[writer]['sum']/wri_avg[writer]['count']
                    
                else:
                     wri_avg[writer]['count'] = wri_avg[writer]['count'] + 1
                     wri_avg[writer]['sum'] = wri_avg[writer]['sum'] + writers[writer] 
                     wri_avg[writer]['avg'] = wri_avg[writer]['sum']/wri_avg[writer]['count']
       
            
            genres = training[movie]['genres']
            for genre in genres:
                if genre not in gen_avg:
                    gen_avg[genre] = {}
                    gen_avg[genre]['count'] = 1
                    gen_avg[genre]['sum'] = genres[genre]
                    gen_avg[genre]['avg'] = gen_avg[genre]['sum']/gen_avg[genre]['count']
                    
                else:
                     gen_avg[genre]['count'] = gen_avg[genre]['count'] + 1
                     gen_avg[genre]['sum'] = gen_avg[genre]['sum'] + genres[genre] 
                     gen_avg[genre]['avg'] = gen_avg[genre]['sum']/gen_avg[genre]['count']

            plots = training[movie]['plot']
            for plotword in plots:
                if plotword not in plot_avg:
                    plot_avg[plotword] = {}
                    plot_avg[plotword]['count'] = 1
                    plot_avg[plotword]['sum'] = plots[plotword]
                    plot_avg[plotword]['avg'] = plot_avg[plotword]['sum']/plot_avg[plotword]['count']
                    
                else:
                     plot_avg[plotword]['count'] = plot_avg[plotword]['count'] + 1
                     plot_avg[plotword]['sum'] = plot_avg[plotword]['sum'] + plots[plotword] 
                     plot_avg[plotword]['avg'] = plot_avg[plotword]['sum']/plot_avg[plotword]['count']

            if 'rating_count' in training[movie]:
                if training[movie]['rating_count'] > rmax:
                    rmax = training[movie]['rating_count'] 
                
        self.plot_avg = plot_avg
        self.gen_avg = gen_avg
        self.wri_avg = wri_avg
        self.dir_avg = dir_avg
        self.actor_avg = actor_avg
        self.avgrating = rating_sum/rcount
        self.avgcount = countsum/rcount
        self.max = rmax

    def classify(self, current, vspace):
        #current is the movie we want to classify against training set

        actorlist = current[vspace]
        #print vspace
        #print actorlist
        curdict = {}
        if vspace == "plot":
            curdict = self.plot_avg
        elif vspace == "genres":
            curdict = self.gen_avg
        elif vspace == "writers":
            curdict = self.wri_avg
        elif vspace == "directors":
            curdict = self.dir_avg
        else:
            curdict = self.actor_avg

        maxx = self.max
       
   
        for item in actorlist:
            if item in curdict:
                actorlist[item] = curdict[item]['avg']
            else:
                if vspace == "plot":
                    actorlist[item] = len(item)/((self.avgrating-3)*math.log(self.avgcount-15000,10))/math.log(maxx,15)
                else:
                    actorlist[item] = ((self.avgrating-3)*math.log(self.avgcount-15000,10))/math.log(maxx,15)

            
            

        #print 
        #print actorlist
        #print
        #print "-------------------------------"
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

        list = [classes[id] for id in ids]
            #print list
        common_categorie = self.most_common(list)

        return common_categorie
