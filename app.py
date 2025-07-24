from flask import Flask, request, jsonify, render_template, redirect, url_for
import json, os

app = Flask(__name__)
users_file = 'users.json'

# Load users
def load_users():
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            return json.load(f)
    return {}

# Save users
def save_users(users):
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=4)

# Routes
@app.route('/')
def home():
    return redirect(url_for('signup_page'))

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # You must create this HTML page

# Signup logic
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    users = load_users()

    if username in users:
        return jsonify({"message": "Username already exists."}), 409

    users[username] = {
        "email": email,
        "password": password
    }

    save_users(users)
    return jsonify({"message": "Signup successful!"}), 201

# Login logic
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    users = load_users()

    if username in users and users[username]['password'] == password:
        return jsonify({"message": "Login successful!", "redirect": "/dashboard"}), 200
    else:
        return jsonify({"message": "Invalid username or password."}), 401

if __name__ == '__main__':
    app.run(debug=True)
