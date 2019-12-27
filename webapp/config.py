import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "..", "webapp.db")

SECRET_KEY = "lkdjap;oij;,wd0023)()(2n2n)lkdqwoeqo34>o3k5%"
