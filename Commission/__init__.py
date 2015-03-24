from flask import Flask

from flask_admin import Admin 
from flask_admin.contrib.peewee import ModelView

from models import db, User, Sales

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MYCOMMISSION'

admin = Admin(app, name='Commission Admin')
admin.add_view(ModelView(User))
admin.add_view(ModelView(Sales))

from Commission import views
