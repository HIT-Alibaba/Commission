from flask import Flask, g

from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView

from models import db, User, Sales

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MYCOMMISSION'

class MyModelView(ModelView):

    def is_accessible(self):
        return hasattr(g, 'admin') and g.admin == True

admin = Admin(app, name='Commission Admin')
admin.add_view(MyModelView(User))
admin.add_view(MyModelView(Sales))

from Commission import views
