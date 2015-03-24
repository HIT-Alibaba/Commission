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


class Sales(BaseModel):
    saler_id = peewee.ForeignKeyField(User)
    locks = peewee.IntegerField()
    stocks = peewee.IntegerField()
    barrels = peewee.IntegerField()
    date = peewee.DateTimeField()


class Admin(BaseModel):
    name = peewee.CharField(max_length=64)
    password = peewee.CharField(max_length=64)
