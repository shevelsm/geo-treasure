from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    created = db.Column(db.DateTime)
    role = db.Column(db.String(16), index=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == "admin"

    def __repr__(self):
        return f"User {self.username}"


class Point(db.Model):
    db.__tablename__ = "point"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    source = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    long = db.Column(db.Float, nullable=False)
    info = db.Column(db.Text, nullable=True)
    clusters = db.relationship("ClusterPoint", back_populates="point")

    def __repr__(self):
        return f"<Point {self.title} at {self.lat} {self.long}>"


class Cluster(db.Model):
    db.__tablename____ = "cluster"
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    long = db.Column(db.Float, nullable=False)
    radius = db.Column(db.Float, nullable=False)
    points = db.relationship("ClusterPoint", back_populates="cluster")

    def __rep__(self):
        return f"<Cluster #{self.id}>"


class ClusterPoint(db.Model):
    db.__tablename__ = "cluster_point"
    cluster_id = db.Column(db.Integer, db.ForeignKey("cluster.id"), primary_key=True)
    point_id = db.Column(db.Integer, db.ForeignKey("point.id"), primary_key=True)
    cluster = db.relationship("Cluster", back_populates="points")
    point = db.relationship("Point", back_populates="clusters")
