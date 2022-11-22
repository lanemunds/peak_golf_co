from model import db, User, Putter, connect_to_db, Rating, Used


def create_user(username, email, password):

    user = User(username, email, password)

    return user


def create_putter(name, putter_path, price, company, info):

    putter = Putter(name=name, putter_path=putter_path,
                    price=price, company=company, info=info)
    return putter


def get_putters():
    return Putter.query.all()


def get_users():
    return User.query.all()


def get_used():
    return Used.query.all()


def get_putter_by_id(putter_id):
    return Putter.query.get(putter_id)


def get_rating_by_putter_id(putter_id):
    return Rating.query.filter_by(putter_id=putter_id).all()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_user_by_email(email):
    return User.query.filter(User.email == email).first()


def create_rating(user, putter, score):

    rating = Rating(user=user, putter=putter, score=score)
    return rating


def create_used(user, putter, haveUsed):

    haveUsed = Used(user=user, putter=putter, haveUsed=haveUsed)
    return haveUsed


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
