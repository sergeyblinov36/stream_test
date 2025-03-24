from functools import wraps
from flask import Flask, request, jsonify, abort
import jwt


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


from functools import wraps
from flask import Flask, request, jsonify, abort
import jwt


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization').split(" ")[1]
        decoded = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
        if decoded.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated