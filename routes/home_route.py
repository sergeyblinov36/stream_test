from flask import Blueprint, jsonify, request, render_template

home_bp = Blueprint('home',__name__)

@home_bp.route('/')
def index():
    return render_template('index.html')
