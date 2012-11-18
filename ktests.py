import unittest
import knn
import math

docs = {}
docs['001'] = {'rating': 9.0, 'actors':{'Christian Bale': 0.87, 'Jack Nicholson': 0.76}} 
docs['002'] = {'rating': 8.7, 'actors':{'Dora The Explorer': 0.92, 'Jack Nicholson': 0.51}}
docs['003'] = {'rating': 5.5, 'actors':{'Brad Pitt': 0.92, 'Mohamed Sleem': 0.91}}
docs['004'] = {'rating': 8.8, 'actors':{'Bradley Cooper': 0.882, 'Dora The Explorer': 0.43}}



class TestVectorization(unittest.TestCase):
    def setUp(self):
        self.knn = knn.knn()
   
    def test_euclid_dist(self):
        a = docs['001']['actors']
        b = {'Christian Bale': 0.97, 'Jack Nicholson': 0.16}
        dist = self.knn.euclid(a,b)
        self.assertAlmostEqual(dist,0.608276253)

    def test_classify(self):
        b = {}
        b['actors'] = {'Christian Bale': 0.97, 'Jack Nicholson': 0.16}
        rating = self.knn.classify(docs, b)
        self.assertAlmostEqual(rating, 9.0)

if __name__ == '__main__':
    unittest.main()
