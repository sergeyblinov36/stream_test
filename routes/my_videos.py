from flask import Blueprint, jsonify, session, redirect
from models.video import Video

my_videos_bp = Blueprint('my_videos', __name__)

@my_videos_bp.route('/my_videos', methods=['GET'])
def my_videos():
    if 'user_id' not in session:
        return redirect('/login')  # Redirect to login page if not logged in

    user_id = session['user_id']
    videos = Video.query.filter_by(user_id=user_id).all()
    video_list = [{'filename': v.filename, 'title': v.title, 'description': v.description} for v in videos]
    return jsonify(video_list)