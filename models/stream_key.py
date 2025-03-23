from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class StreamKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<StreamKey {self.key}>'