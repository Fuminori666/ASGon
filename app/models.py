from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    surname = db.Column(db.Text)
    username = db.Column(db.Text, index=True, unique=True)
    email = db.Column(db.Text, index=True, unique=True)
    password_hash = db.Column(db.Text)
    salt = db.Column(db.Text)
    posts = db.relationship("Post", backref='author', lazy='dynamic')
    playerlist = db.relationship("PlayersList", uselist=False, back_populates="User")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        user_hash = generate_password_hash(password, 'sha512')
        array = user_hash.split('$')
        self.password_hash = array[2]
        self.salt = array[1]

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


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
    players = db.relationship("User", back_populates="PlayersList")
    games = db.relationship("Games")
    orderedgames = db.relationship("OrderedGames")

    def __repr__(self):
        return '<PlayersList {}>'.format(self.id_game + ' ' + self.id_player)


class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    games = db.relationship("Games")
    orderedgames = db.relationship("OrderedGames")

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
    service = db.relationship("ServiceList")

    def __repr__(self):
        return '<OrderedGame {}>'.format(self.id_date)


class ServiceList(db.Model):
    __tablename__ = 'servicelist'
    id = db.Column(db.Integer, primary_key=True)
    id_game = db.Column(db.Integer, db.ForeignKey('orderedgames.id'))
    id_service = db.Column(db.Integer, db.ForeignKey('service.id'))
    service = db.relationship("Service", back_populates="ServiceList")

    def __repr__(self):
        return '<ServiceList {}>'.format(self.id_game + ' ' + self.id_service)


class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.Text)
    price = db.Column(db.Text)
    servises = db.relationship("ServiceList", uselist=False, back_populates="Service")

    def __repr__(self):
        return '<Service {}>'.format(self.service_name + ' ' + self.price)
