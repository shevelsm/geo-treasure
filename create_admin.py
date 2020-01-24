from getpass import getpass
import logging
import sys

from webapp import create_app
from webapp.model import db, User

app = create_app()
with app.app_context():
    username = input("Name: ")

    if User.query.filter(User.username == username).count():
        logging.info("This username is occupied")
        sys.exit(0)

    password1 = getpass("Create password: ")
    password2 = getpass("Confirm password: ")

    if not password1 == password2:
        logging.info("Passwords are not matched")
        sys.exit(0)

    new_user = User(username=username, email="geo-treasure@inbox.ru", role="admin")
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    logging.info("The admin has been created >> id={}".format(new_user.id))
