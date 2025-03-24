from flask import Blueprint, jsonify, request, abort
from models.stream_key import db, StreamKey  # Import the database model

auth_stream_key_bp = Blueprint('auth_stream_key',__name__)

@auth_stream_key_bp.route('/authenticate_stream_key', methods=['POST'])
def authenticate():
    stream_key = request.args.get('name')  # OBS sends the stream key as 'name'
    key = StreamKey.query.filter_by(key=stream_key).first()
    if key:
        return 'OK', 200  # Authentication success
    else:
        abort(403)  # Forbidden: Invalid key