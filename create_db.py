from webapp.app import db, app


db.create_all(app=app)
