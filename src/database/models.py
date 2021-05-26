from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from time import time
from src import db
from src import login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), index=True, unique=True)
    email = db.Column(db.String(length=50), index=True, unique=True)
    password_hash = db.Column(db.String(length=60))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login_manager.user_loader
def load_user(id):

    return User.query.get(int(id))

class Watchlist(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer(), nullable=False, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def __repr__(self):
        return '<User {}>'.format(self.movie_id)


