from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from flask import send_file


media_bp = Blueprint('media', __name__, url_prefix='/media')
UPLOAD_FOLDER = 'uploads'  # Define upload folder
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}  # Allowed file extensions

# Ensure the folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
print(f"Upload folder: {UPLOAD_FOLDER}")  # Debug: Log the upload folder
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @media_bp.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(UPLOAD_FOLDER, filename)
#         file.save(filepath)
#         return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 201

    # return jsonify({'error': 'Invalid file type'}), 400

@media_bp.route('/upload', methods=['POST'])
def upload_file():
    print("Upload route accessed")  # Debug: Log that the route is reached
    
    if 'file' not in request.files:
        print("No 'file' key in request.files")  # Debug: Log missing file
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    print(f"File received: {file.filename}")  # Debug: Log file name received

    if file.filename == '':
        print("No file selected")  # Debug: Log if no file was selected
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        print(f"Saving file to: {filepath}")  # Debug: Log file save path
        file.save(filepath)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 201

    print("Invalid file type")  # Debug: Log invalid file type
    return jsonify({'error': 'Invalid file type'}), 400

@media_bp.route('/play/<filename>', methods=['GET'])
def play_video(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    print(f"Requested video: {filename}")  # Debugging print
    print(f"Full path: {filepath}")  # Debugging print

    if os.path.exists(filepath):
        print(f"Serving video: {filepath}")  # Debugging print

        return send_file(filepath, mimetype='video/mp4')
    print(f"File not found: {filepath}")  # Debugging print

    return jsonify({'error': 'File not found'}), 404

@media_bp.route('/test', methods=['GET'])
def test_route():
    return jsonify({'message': 'Route is working'})

import os

@media_bp.route('/list_videos', methods=['GET'])
def list_videos():
    files = os.listdir(UPLOAD_FOLDER)
    video_files = [f for f in files if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
    return jsonify(video_files)