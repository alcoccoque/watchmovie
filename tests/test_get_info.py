import unittest
from get_info import get_cast_info, get_movie_info, get_reviews_info, get_recommends_info, get_info
# from ml.trained_model import load
import tmdbv3api as tmdb3

tmdb = tmdb3.TMDb()
tmdb.api_key = 'df67c6cc529840b0a18cd7017e1f2fd1'
movie = tmdb3.Movie()
person = tmdb3.Person()
# filename, clf, vectorizer = load()


test_cast_13564 = ({'Amanda Righetti': [74289, 'Ariel Wolfe',
                                   'https://image.tmdb.org/t/p/original/glAhErOplmToSjCf5QB8mjAnuXt.jpg']},
              {'Amanda Righetti': [74289, 'https://image.tmdb.org/t/p/original/glAhErOplmToSjCf5QB8mjAnuXt.jpg',
                                   '1983-04-04', 'St. George, Utah, USA', 'Amanda Righetti is an American actress and film producer, best known for her roles in The Mentalist, Friday the 13th and The O.C..']})

test_movie_13564 = ('Return to House on Haunted Hill',
                    'https://image.tmdb.org/t/p/original/ipBiyifbFqY0ZduO3R9OPBjc2pH.jpg',
                    9.65, ['Horror', 'Thriller'], "Eight years have passed since Sara Wolfe and Eddie Baker "
                                                  "escaped the House on Haunted Hill. Now the kidnapped Ariel,"
                                                  " Sara's sister, goes inside the house with a group of treasure "
                                                  "hunters to find the statue of Baphomet, worth millions and believed "
                                                  "to be the cause of the House's evil.",
                    5.4, 165, '2007-10-03', '1 hour(s) 21 min(s)', 'Released', 13564)

test_reviews_13564 = {"The movie starts alright by creating some tension but then descends into a paint by numbers. "
                      "There is some good to be said: The acting is fair, the special effects adequate and the "
                      "cinematography competent. However, the movie disregards one of the main rules of horror "
                      "in my book: Scares in a haunted house are achieved through subtlety. Mr. García seems to "
                      "have been involved mainly in special effects before and he shows it with too much pride. "
                      "While the effects are well done, nothing here happens in the shadows, everything has a spot "
                      "on it. It's like the director wanted to showcase his handwork but in doing so, he degrades "
                      "it to mere circus tricks (albeit bloody ones). He's even confident enough to leave the door "
                      "open for another sequel. Final judgment: Nothing outstanding but not too weak either. I was "
                      "mildly interested to watch until the end - 5,5/10.": 'positive',
                      'I am giving this a 6 out of 10 because the movie had enough going on not to make me want '
                      'to shut it off half way through. With that being said, I must say I am disappointed on how '
                      'the characters get into the house so easily. Seriously, most of us as viewers are not idiots, '
                      'and with what had happened in that house, I know it would there would have been some type of '
                      'guard or security company working there. Second, they could have made the reason for the house '
                      'being evil a little better then the Indiana Jones deal. But, for a DTV this is an okay movie '
                      'that I think fills in the void for lack of gore movies. There are some good blood and '
                      'guts scenes. So rent it and take the movie for what it is.':
                      'positive', "Okay, where to start... First off, there is no lead in on how the house became "
                      "reopened. How did it open up after going into lock down to start? The whole obsessed sister "
                      "thing is a poor way to kick off the beginning as well. Then who shoots the hell out of gears "
                      "to stop Hill Ouse from going on lock down again, come on... I couldn't go further than the "
                      "betrayal of the Professor before I had to flat out stop it.... If you're going to do a "
                      "sequel you might want to get some things right.": 'positive'}

test_recommends_13564 = '<zip object at 0x000001D6C7817B40>'

class TestGetCastInfo(unittest.TestCase):
    def test_get_cast_info(self):
        movie = tmdb3.Movie()
        self.assertEqual(get_cast_info(movie.credits(13564).cast[:1]), test_cast_13564)
        self.assertEqual(get_cast_info(movie.credits('13564').cast[:1]), test_cast_13564)

    def test_invalid_get_cast_info(self):
        movie = tmdb3.Movie()
        self.assertRaises(ValueError, get_cast_info, movie.credits('asd'))
        self.assertRaises(ValueError, get_cast_info, movie.credits(''))
        self.assertRaises(ValueError, get_cast_info, movie.credits('--@!Sda'))
        self.assertRaises(ValueError, get_cast_info, movie.credits(True))

class TestGetMovieInfo(unittest.TestCase):
    def test_get_movie_info(self):
        movie = tmdb3.Movie()
        self.assertEqual(get_movie_info(movie.details(13564)), test_movie_13564)
        self.assertEqual(get_movie_info(movie.details('13564')), test_movie_13564)

    def test_invalid_get_movie_info(self):
        movie = tmdb3.Movie()
        self.assertRaises(ValueError, get_movie_info, movie.details('asd'))
        self.assertRaises(ValueError, get_movie_info, movie.details(''))
        self.assertRaises(ValueError, get_movie_info, movie.details('--@!Sda'))
        self.assertRaises(ValueError, get_movie_info, movie.details(False))

class TestGetReviewsInfo(unittest.TestCase):
    def test_get_reviews_info(self):
        movie = tmdb3.Movie()
        self.assertEqual(get_reviews_info(movie.details(13564)), test_reviews_13564)
        self.assertEqual(get_reviews_info(movie.details('13564')), test_reviews_13564)

    def test_invalid_get_reviews_info(self):
        movie = tmdb3.Movie()
        self.assertRaises(ValueError, get_reviews_info, movie.details('asd'))
        self.assertRaises(ValueError, get_reviews_info, movie.details(''))
        self.assertRaises(ValueError, get_reviews_info, movie.details('--@!Sda'))
        self.assertRaises(ValueError, get_reviews_info, movie.details(False))

class TestGetRecommendsInfo(unittest.TestCase):
    def test_get_reviews_info(self):
        movie = tmdb3.Movie()
        self.assertEqual(get_recommends_info(movie.details(13564)), test_recommends_13564)
        self.assertEqual(get_recommends_info(movie.details('13564')), test_recommends_13564)

    def test_invalid_get_reviews_info(self):
        movie = tmdb3.Movie()
        self.assertRaises(ValueError, get_recommends_info, movie.details('asd'))
        self.assertRaises(ValueError, get_recommends_info, movie.details(''))
        self.assertRaises(ValueError, get_recommends_info, movie.details('--@!Sda'))
        self.assertRaises(ValueError, get_recommends_info, movie.details(True))

class TestGetInfo(unittest.TestCase):
    def test_get_info(self):
        movie = tmdb3.Movie()
        self.assertEqual(get_info(movie.details(13564)), test_recommends_13564)
        self.assertEqual(get_info(movie.details('13564')), test_recommends_13564)

    def test_invalid_get_info(self):
        movie = tmdb3.Movie()
        self.assertRaises(ValueError, get_info, movie.details('asd', ''))
        self.assertRaises(ValueError, get_info, movie.details('', ''))
        self.assertRaises(ValueError, get_info, movie.details('--@!Sda', 123))