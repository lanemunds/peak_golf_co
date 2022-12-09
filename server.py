from flask import Flask, render_template, redirect, flash, request, session, url_for
from jinja2 import StrictUndefined
from random import randint
import crud
from model import connect_to_db, db

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    putter = crud.get_putter_by_id(randint(1, 15))
    return render_template("index.html", putter=putter)


@ app.route('/putters')
def putter_page():
    clubs = crud.get_putters()
    return render_template("putters.html", clubs=clubs)


@ app.route('/login')
def login_page():
    return render_template("login.html")


@ app.route('/create_account')
def create_account_page():
    return render_template("create_account.html")


@ app.route('/putters/<putter_id>')
def specs_page(putter_id):
    putter = crud.get_putter_by_id(putter_id)
    used = crud.get_used()
    people = crud.get_users()
    ratings = crud.get_rating_by_putter_id(putter_id)
    total = 0
    for rating in ratings:
        total = total + rating.score
    if len(ratings) != 0:
        avg = total/len(ratings)
    else:
        avg = -1

    return render_template("putter_specs.html", putter=putter, used=used, people=people, avg=avg)


@ app.route("/users", methods=["POST"])
def register_user():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash(
            "Account with that email already exists. Please log in or try a different email")
        return redirect('/create_account')
    else:
        user = crud.create_user(username, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
    return redirect('/login')


@ app.route("/login", methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash("The email or password you entered was incorrect")
    else:
        session['user_email'] = user.email
        flash(f"Welcome Back,{user.username}!")
    return redirect("/")


@ app.route("/logout")
def logout():
    del session['user_email']
    session["cart"] = {}
    flash("You're logged out")
    return redirect("/")


@ app.route('/cart')
def cartPage():
    if 'user_email' not in session:
        return redirect('/login')
    order_total = 0
    cart_putters = []
    cart = session.get("cart", {})
    for putter_id, quantity in cart.items():
        putter = crud.get_putter_by_id(putter_id)

        total_cost = quantity * putter.price
        order_total += total_cost

        putter.quantity = quantity
        putter.total_cost = total_cost

        cart_putters.append(putter)

    return render_template("cart.html", cart_putters=cart_putters, order_total=order_total)


@ app.route('/add_to_cart/<putter_id>')
def add_to_cart(putter_id):
    if 'user_email' not in session:
        return redirect('/login')
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    cart[putter_id] = cart.get(putter_id, 0) + 1
    session.modified = True
    flash(f"Putter {putter_id} successfully added to cart.")
    print(cart)

    return redirect("/cart")


@ app.route("/empty-cart")
def empty_cart():
    session["cart"] = {}

    return redirect("/cart")


@ app.route("/putters/<putter_id>/ratings", methods=["POST"])
def create_rating(putter_id):

    logged_in_email = session.get("user_email")
    rating_score = request.form.get("rating")

    if logged_in_email is None:
        flash("You must log in to rate a putter.")
    elif not rating_score:
        flash("Error: you didn't select a score for your rating.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        putter = crud.get_putter_by_id(putter_id)

        rating = crud.create_rating(user, putter, int(rating_score))
        db.session.add(rating)
        db.session.commit()

        flash(f"You rated this putter {rating_score} out of 5.")

    return redirect(f"/putters/{putter_id}")


@ app.route("/putters/<putter_id>/used", methods=["POST"])
def haveYouUsed(putter_id):

    logged_in_email = session.get("user_email")
    have_used = request.form.get("used")

    if logged_in_email is None:
        flash("You must log in to mark a club as used.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        putter = crud.get_putter_by_id(putter_id)

        used = crud.create_used(user, putter, bool(have_used))
        db.session.add(used)
        db.session.commit()

        flash(f"You rated this putter {have_used}.")

    return redirect(f"/putters/{putter_id}")


@ app.route("/users")
def all_users():

    users = crud.get_users()

    return render_template("users.html", users=users)


@ app.route("/users/<user_id>")
def show_user(user_id):

    user = crud.get_user_by_id(user_id)

    return render_template("user_page.html", user=user)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, port=8050)
