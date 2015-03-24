from Commission.models import db, User, Sales, Admin


if __name__ == '__main__':
    User.create_table()
    Sales.create_table()
    Admin.create_table()
