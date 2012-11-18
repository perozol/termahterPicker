import unittest
import vectorization
import math

movies = [
    {"rating": 9.0, "genres": ["Action", "Crime", "Drama", "Thriller"], "rated": "PG_13", "language": ["English", "Mandarin"], "title": "The Dark Knight", "poster": "http://ia.media-imdb.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1._SY317_CR0,0,214,317_.jpg", "imdb_url": "http://www.imdb.com/title/tt0468569/", "directors": ["Christopher Nolan"], "also_known_as": ["Batman: The Dark Knight"], "imdb_id": "tt0468569", "country": ["USA", "UK"], "filming_locations": "2 International Finance Centre, Central, Hong Kong, China", "writers": ["Jonathan Nolan", "Christopher Nolan"], "actors": ["Christian Bale", "Heath Ledger", "Aaron Eckhart", "Michael Caine", "Maggie Gyllenhaal", "Gary Oldman", "Morgan Freeman", "Monique Gabriela Curnen", "Ron Dean", "Cillian Murphy", "Chin Han", "Nestor Carbonell", "Eric Roberts", "Ritchie Coster", "Anthony Michael Hall"], "plot_simple": "When Batman, Gordon and Harvey Dent launch an assault on the mob, they let the clown out of the box, the Joker, bent on turning Gotham on itself and bringing any heroes down to his level.", "year": 2008, "runtime": ["152 min"], "type": "M", "release_date": 20080718, "rating_count": 832786},
    {"rating": 6.4, "genres": ["Drama", "Music"], "rated": "PG_13", "language": ["English"], "title": "Swing Kids", "poster": "http://ia.media-imdb.com/images/M/MV5BMTQ4NDAxNjA5NF5BMl5BanBnXkFtZTcwMzUyNTUyMQ@@._V1._SY317_CR3,0,214,317_.jpg", "imdb_url": "http://www.imdb.com/title/tt0108265/", "directors": ["Thomas Carter"], "imdb_id": "tt0108265", "country": ["USA"], "filming_locations": "Prague, Czech Republic", "rating_count": 9610, "actors": ["Robert Sean Leonard", "Christian Bale", "Frank Whaley", "Barbara Hershey", "Tushka Bergen", "David Tom", "Julia Stemberger", "Jayce Bartok", "Noah Wyle", "Johan Leysen", "Douglas Roberts", "Martin Clunes", "Jessica Hynes", "Carl Brincat", "Mary Fogarty"], "plot_simple": "The story of a close-knit group of young kids in Nazi Germany who listen to banned swing music from the US...", "year": 1993, "runtime": ["112 min"], "type": "M", "release_date": 19930305, "also_known_as": ["Djeca swinga"]},
    {"rating": 5.4, "genres": ["Drama", "Horror", "Thriller"], "rated": "R", "language": ["English"], "title": "Halloween H20: 20 Years Later", "poster": "http://ia.media-imdb.com/images/M/MV5BMjA1NjMyMTkwN15BMl5BanBnXkFtZTcwNDI1NzEyMQ@@._V1._SY317_CR4,0,214,317_.jpg", "imdb_url": "http://www.imdb.com/title/tt0120694/", "directors": ["Steve Miner"], "also_known_as": ["Halloween: H20"], "imdb_id": "tt0120694", "country": ["USA"], "filming_locations": "Canfield-Moreno Estate - 1923 Micheltorena Street, Silver Lake, Los Angeles, California, USA", "writers": ["Debra Hill", "John Carpenter"], "actors": ["Jamie Lee Curtis", "Adam Arkin", "Michelle Williams", "Adam Hann-Byrd", "Jodi Lyn O'Keefe", "Janet Leigh", "Josh Hartnett", "LL Cool J", "Joseph Gordon-Levitt", "Branden Williams", "Nancy Stephens", "Beau Billingslea", "Matt Winston", "Larisa Miller", "Emmalee Thompson"], "plot_simple": "Laurie Strode, now the dean of a Northern California private school with an assumed name, must battle the Shape one last time and now the life of her own son hangs in the balance.", "year": 1998, "runtime": ["86 min"], "type": "M", "release_date": 19980805, "rating_count": 32425}
]


class TestVectorization(unittest.TestCase):
    def setUp(self):
        self.vector = vectorization.vector()
        self.vector.vectorize(iter(movies))
    
    def test_actor_vector_length(self):
        vectors = self.vector.movie_vectors[movies[0]['imdb_id']]
        length = len(vectors['actors'])
        self.assertEqual(length,15)

    def test_actor_score(self):
        vectors = self.vector.movie_vectors[movies[0]['imdb_id']]
        actors = vectors['actors']
        self.assertAlmostEqual(actors['Michael Caine'], 0.09564422274326599)

    def test_writer_score(self):
        vectors = self.vector.movie_vectors[movies[2]['imdb_id']]
        writers = vectors['writers']
        self.assertAlmostEqual(writers['Debra Hill'], 0.02)

    

if __name__ == '__main__':
    unittest.main()