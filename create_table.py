from Commission.models import db, User, Sale, Admin


if __name__ == '__main__':
    User.create_table()
    Sale.create_table()
    Admin.create_table()
