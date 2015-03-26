import peewee

db = peewee.SqliteDatabase('db.sqlite', check_same_thread=False)


class BaseModel(peewee.Model):

    class Meta:
        database = db


class User(BaseModel):
    id = peewee.PrimaryKeyField()
    username = peewee.CharField(max_length=64)
    password = peewee.CharField(max_length=64)
    level = peewee.IntegerField()


class Sale(BaseModel):
    saler = peewee.ForeignKeyField(User, related_name='sales')
    locks = peewee.IntegerField()
    stocks = peewee.IntegerField()
    barrels = peewee.IntegerField()
    date = peewee.DateField()


class Admin(BaseModel):
    name = peewee.CharField(max_length=64)
    password = peewee.CharField(max_length=64)
