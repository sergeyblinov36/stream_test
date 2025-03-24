from flask import Blueprint, jsonify, request

home_bp = Blueprint('home',__name__)

@home_bp.route('/')
def home():
    return 'Welcome to My Flask App!'