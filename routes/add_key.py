from flask import Blueprint, jsonify, request, abort
from models.stream_key import db, StreamKey

stream_key_bp = Blueprint('add_stream_key', __name__)

@stream_key_bp.route('/add_stream_key', methods=['POST'])
def add_stream_key():
    key = request.json.get('key')  # Get the stream key from the JSON payload
    if key:
        new_key = StreamKey(key=key)
        db.session.add(new_key)
        db.session.commit()
        return jsonify({'message': 'Stream key added successfully!'}), 201
    else:
        return jsonify({'error': 'Stream key is required!'}), 400
    
    