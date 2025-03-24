from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Blueprint, jsonify, request
from decorators.decorators import token_required, admin_required
from static.limiter import limiter

secure_bp = Blueprint('secure', __name__)


@secure_bp.route('/secure_endpoint', methods=['GET'])
@limiter.limit("10 per minute")  # Customize limits
@token_required
def secure_endpoint():
    return jsonify({'message': 'This is a secure endpoint'})