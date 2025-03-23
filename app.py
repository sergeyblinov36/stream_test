# from flask import Flask, request, jsonify, abort
# from flask_sqlalchemy import SQLAlchemy
# from models.stream_key import StreamKey

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stream_keys.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)

# # Create tables
# with app.app_context():
#      db.create_all()

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return 'Welcome to My Flask App!'

# @app.route('/authenticate_stream_key', methods=['POST'])
# def authenticate():
#     stream_key = request.args.get('name')  # OBS sends the stream key as 'name'
#     valid_stream_key = 'your_secret_key'   # Replace with your desired key

#     if stream_key == valid_stream_key:
#         return 'OK', 200  # Authentication success
#     else:
#         abort(403)        # Forbidden: Invalid key

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from models.stream_key import db, StreamKey  # Import the database model


app = Flask(__name__)
app.config.from_object('config.Config')  # Load settings from config.py
db.init_app(app)  # Initialize the database with the Flask app
# db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
# from models.stream_key import db
# print(db.metadata.tables)
@app.route('/')
def home():
    return 'Welcome to My Flask App!'

@app.route('/authenticate_stream_key', methods=['POST'])
def authenticate():
    stream_key = request.args.get('name')  # OBS sends the stream key as 'name'
    key = StreamKey.query.filter_by(key=stream_key).first()
    if key:
        return 'OK', 200  # Authentication success
    else:
        abort(403)  # Forbidden: Invalid key

@app.route('/add_stream_key', methods=['POST'])
def add_stream_key():
    key = request.json.get('key')  # Get the stream key from the JSON payload
    if key:
        new_key = StreamKey(key=key)
        db.session.add(new_key)
        db.session.commit()
        return jsonify({'message': 'Stream key added successfully!'}), 201
    else:
        return jsonify({'error': 'Stream key is required!'}), 400

with app.app_context():
    db.create_all()  # Create database tables if they don't exist

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    