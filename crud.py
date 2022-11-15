from model import db, User, Putter, connect_to_db


def create_user(username, email, password):

    user = User(username=username, email=email, password=password)

    return user


def create_putter(name, putter_path, price, company):

    putter = Putter(name=name, putter_path=putter_path, price = price, company = company)


def get_putters():
    return Putter.query.all


def get_putter_by_id(putter_id):
    return Putter.query.get(putter_id)


def get_user_by_email(email):
    return User.query.filter(User.email == email).first()


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
