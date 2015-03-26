from flask import Flask, g

from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView

from models import db, User, Sale

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MYCOMMISSION'

class MyModelView(ModelView):
    pass

admin = Admin(app, name='Commission Admin')
admin.add_view(MyModelView(User))
admin.add_view(MyModelView(Sale))

from Commission import views
