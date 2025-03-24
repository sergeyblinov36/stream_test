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