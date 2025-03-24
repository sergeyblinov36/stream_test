from flask_sqlalchemy import SQLAlchemy
from models.user import db
# db = SQLAlchemy()  # Define db locally to prevent circular import
# from models.user import User  # Ensure User is imported correctly


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(128), nullable=True)  # Optional: add title support
    description = db.Column(db.String(256), nullable=True)  # Optional: add descriptions
    upload_date = db.Column(db.DateTime, default=db.func.now())  # Add timestamps
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('videos', lazy=True))

    def __repr__(self):
        return f'<Video {self.filename}>'

    @property
    def user(self):
        from models.user import User  # Lazy import
        return User.query.get(self.user_id)
