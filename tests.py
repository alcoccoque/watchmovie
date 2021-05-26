from datetime import datetime, timedelta
import unittest
from src import create_app, db
from src.database.models import User, Watchlist
from config import Config
from wsgi import app

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_URL = None


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

    def test_make_unique_nickname(self):
        u = User(nickname='jo', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname('john')
        assert nickname != 'john'
        u = User(nickname=nickname, email='susan@example.com')
        db.session.add(u)
        db.session.commit()
        nickname2 = User.make_unique_nickname('john')
        assert nickname2 != 'john'
        assert nickname2 != nickname

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

class MainModelCase(unittest.TestCase):

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

    def test_search(self):
        tester = app.test_client(self)
        response = tester.get('main/search', content_type='html/text')
        self.assertEqual(response.status_code, 200)

class TestNotRenderTemplates(unittest.TestCase):
    render_templates = False

    def test_assert_home_template_used(self):
        response = self.client.get("/index")
        self.assert_template_used('home.html')

    def test_assert_home_template_used(self):
        response = self.client.get("/auth/login")
        self.assert_template_used('login.html')

    def test_assert_home_template_used(self):
        response = self.client.get("/auth/register")
        self.assert_template_used('register.html')

    def test_assert_home_template_used(self):
        response = self.client.get("/main/search")
        self.assert_template_used('search.html')
    # def test_follow_posts(self):
    #     # create four users
    #     u1 = User(username='john', email='john@example.com')
    #     u2 = User(username='susan', email='susan@example.com')
    #     u3 = User(username='mary', email='mary@example.com')
    #     u4 = User(username='david', email='david@example.com')
    #     db.session.add_all([u1, u2, u3, u4])
    #
    #     # create four posts
    #     now = datetime.utcnow()
    #     p1 = Post(body="post from john", author=u1,
    #               timestamp=now + timedelta(seconds=1))
    #     p2 = Post(body="post from susan", author=u2,
    #               timestamp=now + timedelta(seconds=4))
    #     p3 = Post(body="post from mary", author=u3,
    #               timestamp=now + timedelta(seconds=3))
    #     p4 = Post(body="post from david", author=u4,
    #               timestamp=now + timedelta(seconds=2))
    #     db.session.add_all([p1, p2, p3, p4])
    #     db.session.commit()
    #
    #     # setup the followers
    #     u1.follow(u2)  # john follows susan
    #     u1.follow(u4)  # john follows david
    #     u2.follow(u3)  # susan follows mary
    #     u3.follow(u4)  # mary follows david
    #     db.session.commit()
    #
    #     # check the followed posts of each user
    #     f1 = u1.followed_posts().all()
    #     f2 = u2.followed_posts().all()
    #     f3 = u3.followed_posts().all()
    #     f4 = u4.followed_posts().all()
    #     self.assertEqual(f1, [p2, p4, p1])
    #     self.assertEqual(f2, [p2, p3])
    #     self.assertEqual(f3, [p3, p4])
    #     self.assertEqual(f4, [p4])
    #

if __name__ == '__main__':
    unittest.main(verbosity=2)