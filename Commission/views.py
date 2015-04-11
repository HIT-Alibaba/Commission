from datetime import date
from functools import wraps

from Commission import app
from Commission import User, Sale

from flask import render_template, flash, request, g, session, redirect, url_for

from peewee import *

from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, NumberRange

from utils import *


class LoginForm(Form):
    name = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


@app.before_request
def before_request():
    g.user = None
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
    if g.user:
        if g.user.id == 0:
            return redirect(url_for('salesman_index'))
        elif g.user.id == 1:
            return redirect(url_for('gunsmith_index'))

    return redirect(url_for('login'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if g.user:
        if g.user.id == 0:
            return redirect(url_for('salesman_index'))
        elif g.user.id == 1:
            return redirect(url_for('gunsmith_index'))

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
                    session['user_id'] = user.id
                    session['user_level'] = user.level
                    if user.level == 0:
                        return redirect(url_for('salesman_index'))
                    elif user.level == 1:
                        return redirect(url_for('gunsmith_index'))

    if error:
        flash(error, category='error')
    return render_template("login.html", form=form, title="Login")


@app.route('/logout')
def logout():
    """Logs the user out."""
    flash('You were logged out', category='info')
    session.pop('user_id', None)
    session.pop('user_level', None)
    return redirect(url_for('login'))


@login_required
@app.route("/salesman", methods=["GET"])
def salesman_index():
    d = date.today()
    total_locks, total_stocks, total_barrels, early_finish = get_total_sales(
        g.user, d.year, d.month)
    left_locks = AVAILABLE_LOCKS - total_locks
    left_stocks = AVAILABLE_STOCKS - total_stocks
    left_barrels = AVAILABLE_BARRELS - total_barrels
    if early_finish:
        left_locks = left_stocks = left_barrels = 0
    print("Early Finish: " + str(early_finish))
    return render_template('salesman_index.html', title="Salesman",
                           left_locks=left_locks, left_stocks=left_stocks, left_barrels=left_barrels, early_finish=early_finish)


@login_required
@app.route("/gunsmith", methods=["GET"])
def gunsmith_index():
    allowed_users = User.select().where(User.level == 0)
    return render_template('gunsmith_index.html', title="Query", users=allowed_users)


@login_required
@app.route("/do_sale", methods=["POST"])
def sale():

    locks = request.form['locks']
    stocks = request.form['stocks']
    barrels = request.form['barrels']

    if int(locks) == -1:
        sale = Sale(saler=g.user.id, locks=-1, stocks=stocks,
                    barrels=barrels, date=date.today())
        sale.save()
        flash("Finish this Month", category='info')
        return redirect(url_for('salesman_index'))

    d = date.today()
    total_locks, total_stocks, total_barrels, early_finish = get_total_sales(
        g.user, d.year, d.month)
    left_locks = AVAILABLE_LOCKS - total_locks
    left_stocks = AVAILABLE_STOCKS - total_stocks
    left_barrels = AVAILABLE_BARRELS - total_barrels

    if int(locks) <= left_locks and int(stocks) <= left_stocks and int(barrels) <= left_barrels:
        sale = Sale(saler=g.user.id, locks=locks, stocks=stocks,
                    barrels=barrels, date=date.today())
        sale.save()
        flash("Success", category='success')
    else:
        flash("Input not valid", category='error')
    return redirect(url_for('salesman_index'))


@login_required
@app.route("/query", methods=["GET"])
def query_sales():
    allowed_users = [g.user]
    return render_template('query_index.html', title="Query", users=allowed_users)


@login_required
@app.route("/do_query", methods=["POST"])
def do_query():
    salesman_id = request.form['id']
    year = int(request.form['year'])
    month = int(request.form['month'])

    start_date = date(year, month, 1)
    if month == 12:
        year += 1
    end_date = date(year, (month + 1) % 12, 1)

    d = date.today()
    if date(year, month, 1) > d:
        flash("Date not valid", category='error')
        return redirect(url_for('query_sales'))

    sales = []
    salesman = User.get(User.id == salesman_id)
    for sale in salesman.sales:
        if start_date <= sale.date < end_date and sale.locks >= 0:
            sales.append(sale)

    total_locks, total_stocks, total_barrels, _ = get_total_sales(
        salesman, year, month)
    commission = get_commission(total_locks, total_stocks, total_barrels)
    return render_template('query_result.html', sales=sorted(sales, key=lambda x:x.date.day), title="Result", total_locks=total_locks, total_stocks=total_stocks, total_barrels=total_barrels, commission=commission)


@login_required
@app.route("/query/this_month", methods=["GET"])
def query_this_month():
    salesman = g.user
    d = date.today()
    start_date = date(d.year, d.month, 1)
    if d.month == 12:
        d.year += 1
    end_date = date(d.year, (d.month + 1) % 12, 1)

    results = []
    for sale in salesman.sales:
        if start_date <= sale.date < end_date and sale.locks >= 0:
            results.append(sale)

    total_locks, total_stocks, total_barrels, _ = get_total_sales(
        salesman, d.year, d.month)
    commission = get_commission(total_locks, total_stocks, total_barrels)
    return render_template('query_result.html', sales=sorted(results, key=lambda x:x.date.day), title="Report", total_locks=total_locks, total_stocks=total_stocks, total_barrels=total_barrels, commission=commission)
