from flask import Blueprint, jsonify, request, render_template, session, redirect
from models.video import Video

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
def dashboard():
    # Ensure the user is logged in
    if 'user_id' not in session:
        return redirect('/login')  # Redirect to login if not authenticated

    # Fetch data for the dashboard (e.g., user's videos)
    user_id = session['user_id']
    videos = Video.query.filter_by(user_id=user_id).all()

    # Pass videos or other relevant data to the template
    return render_template('dashboard.html', videos=videos)