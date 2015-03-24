from datetime import date
from functools import wraps

from Commission import app
from Commission import User, Sales

from flask import render_template, flash, request, g, session, redirect, url_for

from models import User
from peewee import *

from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class LoginForm(Form):
    name = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class SalesForm(Form):
    locks = IntegerField('locks', validators=[NumberRange(0, 70)])
    stocks = IntegerField('stocks', validators=[NumberRange(0, 80)])
    barrels = IntegerField('barrels', validators=[NumberRange(0, 70)])


@app.before_request
def before_request():
    g.user = None
    g.admin = None
    if 'user_id' in session:
        try:
            g.user = User.get(User.id == session['user_id'])
        except DoesNotExist:
            pass


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.admin is None:
            return redirect(url_for('admin_login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = None
    if request.method == 'POST':
        if form.validate_on_submit():
            user = None
            try:
                user = User.get(User.username == request.form['name'])
            except DoesNotExist:
                error = 'Invalid username'

            if user is not None:
                if request.form['password'] != user.password:
                    error = 'Invalid password'
                else:
                    flash('You were logged in')
                    session['user_id'] = user.id
                    session['user_level'] = user.level
                    return redirect(url_for('salesman_index', id=user.id))
    if error:
        flash(error)
    return render_template("login.html", form=form, title="Login")


@app.route("/salesman/<int:id>", methods=["GET"])
def salesman_index(id):
    form = SalesForm()
    return render_template('salesman_index.html', form=form, title="Salesman")


@login_required
@app.route("/do_sale", methods=['POST'])
def sale():
    locks = request.form['locks']
    stocks = request.form['stocks']
    barrels = request.form['barrels']
    sale = Sales(saler_id=g.user.id, locks=locks, stocks=stocks,
                 barrels=barrels, date=date.today())
    sale.save()
    flash("Success")
    return redirect(url_for('salesman_index', id=g.user.id))
