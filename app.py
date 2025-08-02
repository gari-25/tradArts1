from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import json, os
import firebase_admin
from firebase_admin import credentials, auth, exceptions
from firebase_admin.auth import UserNotFoundError
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# --- SECRET KEY ---
# Use environment variable in production
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'super_secret_key_dev')

users_file = 'users.json'

# --- Firebase Initialization ---
def initialize_firebase_app():
    """Initializes the Firebase Admin SDK using a secure method."""
    try:
        firebase_admin.get_app()
        print("Firebase Admin SDK already initialized.")
        return True
    except ValueError:
        pass  # App is not initialized, proceed

    try:
        if 'FIREBASE_ADMIN_CREDENTIALS' in os.environ:
            print("Using Firebase credentials from environment variable.")
            cred_json = json.loads(os.environ['FIREBASE_ADMIN_CREDENTIALS'])
            cred = credentials.Certificate(cred_json)
        else:
            print("Using Firebase credentials from local serviceAccountKey.json file.")
            cred = credentials.Certificate("serviceAccountKey.json")
            
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK initialized successfully.")
        return True
    except FileNotFoundError:
        print("Error: 'serviceAccountKey.json' not found.")
        return False
    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {e}")
        return False

firebase_initialized = initialize_firebase_app()

# --- User JSON File Management ---
def load_users():
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=4)

# --- Routes ---
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
    return render_template('dashboard.html')

@app.route('/artist-dashboard')
def artist_dashboard_route():
    return render_template('artist-dashboard.html')

@app.route('/login-events')
def login_events_page():
    return render_template('login-events.html')

@app.route('/login-register')
def login_register_page():
    return render_template('login-register.html')


# --- Signup Logic ---
@app.route('/signup', methods=['POST'])
def signup():
    if not firebase_initialized:
        return jsonify({"message": "Server configuration error. Please try again later."}), 500

    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    user_type = data.get("user_type")

    users = load_users()

    if username in users:
        return jsonify({"message": "Username already exists."}), 409

    # Check if email already exists in Firebase
    try:
        auth.get_user_by_email(email)
        return jsonify({"message": "Email already registered in Firebase."}), 409
    except UserNotFoundError:
        pass  # Safe to proceed

    try:
        firebase_user = auth.create_user(email=email, password=password)
        firebase_uid = firebase_user.uid
        print(f"Firebase user created: {firebase_uid}")

        # Hash password before saving
        users[username] = {
            "email": email,
            "password": generate_password_hash(password),
            "user_type": user_type,
            "firebase_uid": firebase_uid
        }
        save_users(users)

        custom_token = auth.create_custom_token(firebase_uid)
        if isinstance(custom_token, bytes):
            custom_token = custom_token.decode('utf-8')

        return jsonify({
            "message": "Signup successful!",
            "customToken": custom_token,
            "userType": user_type,
            "email": email
        }), 201

    except exceptions.FirebaseError as e:
        print(f"Firebase Auth error during signup: {e}")
        return jsonify({"message": f"Firebase Auth user creation failed: {str(e)}"}), 500
    except Exception as e:
        print(f"General error during signup: {e}")
        return jsonify({"message": "Unexpected error during signup."}), 500


# --- Login Logic ---
@app.route('/login', methods=['POST'])
def login():
    if not firebase_initialized:
        return jsonify({"message": "Server configuration error. Please try again later."}), 500

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    users = load_users()

    if username not in users:
        return jsonify({"message": "Invalid username or password."}), 401

    user_data = users[username]
    if not check_password_hash(user_data["password"], password):
        return jsonify({"message": "Invalid username or password."}), 401

    email = user_data["email"]
    user_type = user_data["user_type"]
    firebase_uid = user_data.get("firebase_uid")

    if not firebase_uid:
        try:
            firebase_user = auth.get_user_by_email(email)
            firebase_uid = firebase_user.uid
            user_data["firebase_uid"] = firebase_uid
            save_users(users)
        except UserNotFoundError:
            return jsonify({"message": "Firebase user not found."}), 401
        except Exception as e:
            print(f"Error fetching Firebase UID: {e}")
            return jsonify({"message": "Unexpected error during login."}), 500

    try:
        custom_token = auth.create_custom_token(firebase_uid)
        if isinstance(custom_token, bytes):
            custom_token = custom_token.decode('utf-8')

        return jsonify({
            "message": "Login successful!",
            "customToken": custom_token,
            "userType": user_type
        }), 200

    except Exception as e:
        print(f"Error creating custom token: {e}")
        return jsonify({"message": "Unexpected error during login."}), 500


# --- Run Block (Local Dev Only) ---
if __name__ == '__main__':
    print("Running Flask development server.")
    app.run(debug=False)
