from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from models.stream_key import db, StreamKey  # Import the database model
import jwt
from functools import wraps
from models.user import db, User
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import uuid
from flask_migrate import Migrate
import datetime
from routes.auth_routes import auth_bp
from routes.home_route import home_bp
from routes.auth_key import auth_stream_key_bp
from routes.add_key import stream_key_bp
from decorators.decorators import token_required, admin_required
from routes.secure_endpoint import secure_bp
from routes.admin_only import admin_only_bp
from routes.request_reset import request_reset_bp
from routes.reset_password import reset_password_bp
from static.limiter import limiter





app = Flask(__name__)
app.config.from_object('config.Config')  # Load settings from config.py
db.init_app(app)  # Initialize the database with the Flask app
# db = SQLAlchemy(app)
with app.app_context():
    db.create_all()


limiter.init_app(app)


migrate = Migrate(app, db)


app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(auth_stream_key_bp)
app.register_blueprint(stream_key_bp)
app.register_blueprint(secure_bp)
app.register_blueprint(admin_only_bp)
app.register_blueprint(request_reset_bp)
app.register_blueprint(reset_password_bp)




with app.app_context():
    db.create_all()  # Create database tables if they don't exist





import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("my_app")

@app.before_request
def log_request():
    logger.info(f"Request: {request.method} {request.url}")

@app.after_request
def log_response(response):
    logger.info(f"Response: {response.status_code}")
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    