from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    source = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    long = db.Column(db.Float, nullable=False)
    info = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Point {self.title} at {self.lat} {self.long}>"
