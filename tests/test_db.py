import os
import pathlib
import unittest

from flask_login import login_user, logout_user, current_user

from src import create_app, db
from src.database.models import User, Watchlist
from config import Config
from wsgi import app
from src.main.routes import watchlist, delete, post

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_URL = None
    LOGIN_DISABLED = False


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='alcoccoque')
        u.set_password('PASS')
        self.assertFalse(u.check_password('pass'))
        self.assertTrue(u.check_password('PASS'))

    def test_search(self):
        tester = app.test_client(self)
        response = tester.get('main/search', content_type='html/text')
        self.assertEqual(response.status_code, 200)

class WatchModelAddCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_movie_add(self):
        watchlist = Watchlist(user_id=1, movie_id=222222)
        db.session.add(watchlist)
        db.session.commit()

class WatchModelRemoveAddCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        watchlist = Watchlist(user_id=1, movie_id=222222)
        db.session.add(watchlist)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_movie_remove(self):
        movie_id = 222222
        Watchlist.query.filter_by(movie_id=movie_id).delete()
        db.session.commit()

    def test_watchlist_get(self):
        user_id = 1
        films = Watchlist.query.filter_by(user_id=user_id).all()

class MainModelCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        BASE_DIR = pathlib.Path(__file__).parent
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + str(
        BASE_DIR / "data" / "test.db")
        self.app = app.test_client()
        db.create_all()
        user = User(username='asdf', email='asd@gmail.com')
        user.set_password('asdasd')
        db.session.add(user)
        db.session.commit()
        login_user(user)

    def tearDown(self):
        logout_user()
        db.session.remove()
        db.drop_all()

    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/index', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_random(self):

        tester = app.test_client(self)
        response = tester.get('main/random', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        tester = app.test_client(self)
        response = tester.get('main/search', content_type='html/text')
        self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main(verbosity=2)