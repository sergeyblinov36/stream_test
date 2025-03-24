from flask import Blueprint, jsonify, request, render_template, session
from models.user import User, db
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)

# Register GET route to render the register page

@auth_bp.route('/register', methods=['POST'])
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
    

# Login GET route to render the login page

@auth_bp.route('/login', methods=['GET'])
def render_login_page():
    return render_template('login.html')  # Render the login.html page

# Login POST route to authenticate the user

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['user_id'] = user.id  # This is required for authentication
        session['username'] = user.username  # Optional for convenience

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
        return jsonify({'token': token, 'redirect_url': '/dashboard'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
    

