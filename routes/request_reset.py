from flask import Flask, request, jsonify, abort, Blueprint
from models.user import db, User
import uuid

request_reset_bp = Blueprint('request_reset',__name__)


@request_reset_bp.route('/request_reset', methods=['POST'])
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