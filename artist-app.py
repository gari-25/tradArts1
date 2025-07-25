# artist_app.py
from flask import Flask, request, jsonify, render_template, send_from_directory, session
from flask_cors import CORS

app = Flask(__name__, static_folder='static', template_folder='frontend')
CORS(app)
app.secret_key = 'supersecretkey'

# In-memory storage for demo
users = {}
artworks = []
events = []

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if data['username'] in users:
        return jsonify({'message': 'Username already exists'}), 400
    users[data['username']] = data['password']
    return jsonify({'message': 'Registration successful'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if users.get(data['username']) == data['password']:
        session['user'] = data['username']
        return jsonify({'message': 'Login successful'})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/upload_art', methods=['POST'])
def upload_art():
    data = request.get_json()
    if 'user' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    artworks.append({
        'title': data['title'],
        'description': data['description'],
        'image_url': data['image_url'],
        'user': session['user']
    })
    return jsonify({'message': 'Artwork uploaded'})

@app.route('/create_event', methods=['POST'])
def create_event():
    data = request.get_json()
    if 'user' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    events.append({
        'name': data['name'],
        'description': data['description'],
        'location': data['location'],
        'date': data['date'],
        'user': session['user']
    })
    return jsonify({'message': 'Event created'})

@app.route('/dashboard_data')
def dashboard_data():
    user = session.get('user')
    if not user:
        return jsonify({'artworks': [], 'events': []})
    user_arts = [a for a in artworks if a['user'] == user]
    user_events = [e for e in events if e['user'] == user]
    return jsonify({ 'artworks': user_arts, 'events': user_events })

@app.route('/')
def index():
    return 'KalaKosh Artist Backend Running'

if __name__ == '__main__':
    app.run(debug=True)
