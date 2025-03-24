from flask import Flask, request, jsonify, abort, Blueprint
from models.user import db, User

reset_password_bp = Blueprint('reset_password',__name__)


@reset_password_bp.route('/reset_password', methods=['POST'])
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