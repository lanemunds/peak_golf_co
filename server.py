from flask import Flask, render_template, redirect, flash, request, session
from jinja2 import StrictUndefined

import crud
from model import connect_to_db, db

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    return render_template("index.html")


@app.route('/putters')
def putter_page():
    return render_template("putters.html")


@app.route('/login')
def login_page():
    return render_template("login.html")


@app.route('/create_account')
def create_account_page():
    return render_template("create_account.html")


@app.route('/putter<putter_id>')
def specs_page():
    return render_template("putter_specs.html")


@app.route('/cart')
def cart_page():
    return render_template("cart.html")


@app.route("/users", methods=["POST"])
def register_user():
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash(
            "Account with that email already exists. Please log in or try a different email")
        return redirect('/create_account')
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
    return redirect('/loginpage')


@app.route("/login", methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash("The email or password you entered was incorrect")
    else:
        session['user_email'] = user.email
        flash(f"Welcome Back,{user.email}!")
    return redirect("/")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, port=8050)
