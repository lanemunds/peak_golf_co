from flask_sqlalchemy import SQLAlchemy
import os


db = SQLAlchemy()


def connect_to_db(flask_app, db_uri=os.environ['POSTGRES_URI'], echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class Putter(db.Model):

    __tablename__ = "clubs"

    putter_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    putter_path = db.Column(db.String)
    price = db.Column(db.Integer)
    company = db.Column(db.String)

    def __init__(self, name, putter_path, price, company):
        self.name = name
        self.putter_path = putter_path
        self.price = price
        self.company = company

    def __repr__(self):
        return f'<Putter putter_id = {self.putter_id} name = {self.name}'


class Rating(db.Model):
    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer)
    putter_id = db.Column(db.Integer, db.ForeignKey("clubs.putter_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    putter = db.relationship("Putter", backref="ratings")
    user = db.relationship("User", backref="ratings")

    def __repr__(self):
        return f'<Rating rating_id={self.rating_id} score={self.score}>'


class Used(db.Model):
    __tablename__ = 'used'

    used_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    haveUsed = db.Column(db.Boolean)
    putter_id = db.Column(db.Integer, db.ForeignKey("clubs.putter_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    putter = db.relationship("Putter", backref="have-used")
    user = db.relationship("User", backref="have-used")

    def __repr__(self):
        return f'<Used used_id={self.used_id} haveUsed={self.haveUsed}>'


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
