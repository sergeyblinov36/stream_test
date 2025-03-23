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



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')  # Get token from headers
        if not token:
            print("No token provided")  # Debugging
            return jsonify({'error': 'Token is missing'}), 403

        try:
            # Verify the token using your secret key
            print(f"Raw token received: {token}")  # Debugging
            # Extract the token part (after "Bearer ")
            token = token.split(" ")[1] if "Bearer " in token else token
            decoded = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
            print(f"Decoded Token: {decoded}")  # Debugging

        except jwt.ExpiredSignatureError:
            print("Token expired")  # Debugging
            return jsonify({'error': 'Token expired'}), 403
        except jwt.InvalidTokenError:
            print("Invalid token")  # Debugging
            return jsonify({'error': 'Invalid token'}), 403

        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization').split(" ")[1]
        decoded = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
        if decoded.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated


app = Flask(__name__)
app.config.from_object('config.Config')  # Load settings from config.py
db.init_app(app)  # Initialize the database with the Flask app
# db = SQLAlchemy(app)
with app.app_context():
    db.create_all()


limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

migrate = Migrate(app, db)


@app.route('/')
def home():
    return 'Welcome to My Flask App!'


@app.route('/authenticate_stream_key', methods=['POST'])
def authenticate():
    stream_key = request.args.get('name')  # OBS sends the stream key as 'name'
    key = StreamKey.query.filter_by(key=stream_key).first()
    if key:
        return 'OK', 200  # Authentication success
    else:
        abort(403)  # Forbidden: Invalid key


@app.route('/add_stream_key', methods=['POST'])
def add_stream_key():
    key = request.json.get('key')  # Get the stream key from the JSON payload
    if key:
        new_key = StreamKey(key=key)
        db.session.add(new_key)
        db.session.commit()
        return jsonify({'message': 'Stream key added successfully!'}), 201
    else:
        return jsonify({'error': 'Stream key is required!'}), 400
    

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully!'}), 201
    else:
        return jsonify({'error': 'Invalid data'}), 400
    

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = jwt.encode(
            {
                'username': username,  # Include username in token
                'role': user.role,  # Include the user's role in the token
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Set token to expire in 1 hour
            },
            'your_secret_key',  # Use your secret key for signing
            algorithm='HS256'  # Algorithm for token generation
        )

        print(token)
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
    

@app.route('/secure_endpoint', methods=['GET'])
@limiter.limit("10 per minute")  # Customize limits
@token_required
def secure_endpoint():
    return jsonify({'message': 'This is a secure endpoint'})

@app.route('/admin_only', methods=['GET'])
@token_required
@admin_required
def admin_only():
    return jsonify({'message': 'Welcome, Admin!'})


@app.route('/request_reset', methods=['POST'])
def request_reset():
    data = request.json
    username = data.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        user.reset_token = str(uuid.uuid4())  # Generate a reset token
        db.session.commit()
        # Send this reset_token to the user (e.g., via email)
        return jsonify({'message': 'Reset token generated'}), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.json
    reset_token = data.get('reset_token')
    new_password = data.get('new_password')
    user = User.query.filter_by(reset_token=reset_token).first()
    if user:
        user.set_password(new_password)
        user.reset_token = None  # Invalidate the token
        db.session.commit()
        return jsonify({'message': 'Password reset successful'}), 200
    return jsonify({'error': 'Invalid or expired reset token'}), 403
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
    