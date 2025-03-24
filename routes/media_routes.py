from flask import Blueprint, request, jsonify, redirect, render_template
import os
from werkzeug.utils import secure_filename
from flask import send_file
from flask import session
from models.video import Video
from models.user import db


media_bp = Blueprint('media', __name__, url_prefix='/media')
UPLOAD_FOLDER = 'uploads'  # Define upload folder
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}  # Allowed file extensions

# Ensure the folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
print(f"Upload folder: {UPLOAD_FOLDER}")  # Debug: Log the upload folder
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define the upload route

# @media_bp.route('/upload', methods=['POST'])
# def upload_file():
#     print("Upload route accessed")  # Debug: Log that the route is reached

#     # Ensure the user is logged in
#     if 'user_id' not in session:
#         print("User not logged in")  # Debug: Log missing user session
#         return jsonify({'error': 'User not logged in'}), 401

#     # Check if the file exists in the request
#     if 'file' not in request.files:
#         print("No 'file' key in request.files")  # Debug: Log missing file
#         return jsonify({'error': 'No file part'}), 400

#     file = request.files['file']
#     print(f"File received: {file.filename}")  # Debug: Log file name received

#     if file.filename == '':
#         print("No file selected")  # Debug: Log if no file was selected
#         return jsonify({'error': 'No selected file'}), 400

#     if file and allowed_file(file.filename):
#         # Generate a secure filename and save the file
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(UPLOAD_FOLDER, filename)
#         print(f"Saving file to: {filepath}")  # Debug: Log file save path
#         file.save(filepath)

#         # Link the file to the logged-in user
#         video = Video(filename=filename, user_id=session['user_id'])  # Associate with user
#         db.session.add(video)
#         db.session.commit()
#         print(f"Video saved in database: {filename}, User ID: {session['user_id']}")  # Debug

#         return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 201

#     print("Invalid file type")  # Debug: Log invalid file type
#     return jsonify({'error': 'Invalid file type'}), 400

@media_bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'user_id' not in session:
        return redirect('/login')  # Redirect if not logged in

    if request.method == 'POST':
        # Validate the file in the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Check if the file type is allowed
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            # Save the file
            file.save(filepath)

            # Save video record in the database
            video = Video(filename=filename, user_id=session['user_id'])
            db.session.add(video)
            db.session.commit()

            return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 201

        return jsonify({'error': 'Invalid file type'}), 400

    return render_template('upload.html')  # Display the upload form

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

# Define a test route

@media_bp.route('/test', methods=['GET'])
def test_route():
    return jsonify({'message': 'Route is working'})



# Define a route to list uploaded videos


@media_bp.route('/list_videos', methods=['GET'])
def list_videos():
    files = os.listdir(UPLOAD_FOLDER)
    video_files = [f for f in files if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
    return jsonify(video_files)

@media_bp.route('/delete_video/<int:video_id>', methods=['DELETE'])
def delete_video(video_id):
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    # Locate the video
    video = Video.query.get(video_id)
    if video and video.user_id == session['user_id']:
        db.session.delete(video)
        db.session.commit()
        return jsonify({'message': 'Video deleted successfully'}), 200

    return jsonify({'error': 'Unauthorized or video not found'}), 404