from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define your database model here
# Example: class Item(db.Model):

class todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    day = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<ToDo {self.name}>'