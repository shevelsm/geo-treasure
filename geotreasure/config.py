import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "..", "geotreasure.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "&,aowbp#X*%!+CiwMD<@X1Z`'<S0\i$"