from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define your database model here
# Example: class Item(db.Model):

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=True)
    publisher = db.Column(db.String(100), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, default=True)

    def __repr__(self):
        return f'<Task {self.title}>'