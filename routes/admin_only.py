from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Blueprint, jsonify, request
from decorators.decorators import token_required, admin_required
from static.limiter import limiter


admin_only_bp = Blueprint('admin_only', __name__)

@admin_only_bp.route('/admin_only', methods=['GET'])
@token_required
@admin_required
def admin_only():
    return jsonify({'message': 'Welcome, Admin!'})