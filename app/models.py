from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    surname = db.Column(db.Text)
    username = db.Column(db.Text, index=True, unique=True)
    email = db.Column(db.Text, index=True, unique=True)
    password_hash = db.Column(db.Text)
    salt = db.Column(db.Text)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        user_hash = generate_password_hash(password, 'sha512', salt_length=8)
        array = user_hash.split('$')
        self.password_hash = array[2]
        self.salt = array[1]

    def check_password(self, password):
        result_hash = 'sha512'+'$'+self.salt+'$'+self.password_hash
        return check_password_hash(result_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    id_creator = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.title + ' ' + self.description)


class PlayersList(db.Model):
    __tablename__ = 'playerslist'
    id = db.Column(db.Integer, primary_key=True)
    id_game = db.Column(db.Integer, db.ForeignKey('games.id'))
    id_player = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<PlayersList {}>'.format(self.id_game + ' ' + self.id_player)


class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Schedule {}>'.format(self.date)


class Games(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    id_date = db.Column(db.Integer, db.ForeignKey('schedule.id'))

    def __repr__(self):
        return '<Games {}>'.format(self.id_date)


class OrderedGames(db.Model):
    __tablename__ = 'orderedgames'
    id = db.Column(db.Integer, primary_key=True)
    id_date = db.Column(db.Integer, db.ForeignKey('schedule.id'))

    def __repr__(self):
        return '<OrderedGame {}>'.format(self.id_date)


class ServiceList(db.Model):
    __tablename__ = 'servicelist'
    id = db.Column(db.Integer, primary_key=True)
    id_game = db.Column(db.Integer, db.ForeignKey('orderedgames.id'))
    id_service = db.Column(db.Integer, db.ForeignKey('service.id'))

    def __repr__(self):
        return '<ServiceList {}>'.format(self.id_game + ' ' + self.id_service)


class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.Text)
    price = db.Column(db.Text)

    def __repr__(self):
        return '<Service {}>'.format(self.service_name + ' ' + self.price)

