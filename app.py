from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin.auth import UserNotFoundError
from firebase_admin import exceptions

# --- Flask App Initialization ---
app = Flask(__name__)
# Use a strong secret key for production, this is for development
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'super_secret_key_dev')

# --- File paths ---
users_file = 'users.json'

# --- Firebase Admin SDK Initialization ---
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
            # IMPORTANT: Replace "serviceAccountKey.json" with the actual path
            cred = credentials.Certificate("serviceAccountKey.json")

        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK initialized successfully.")
        return True
    except FileNotFoundError:
        print("Error: serviceAccountKey.json not found. Please provide the Firebase Admin SDK service account key file.")
        return False
    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {e}")
        return False

# Load users from the JSON file
def load_users():
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            return json.load(f)
    return {}

# Save users to the JSON file
def save_users(users):
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=4)

# --- Routes ---

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Signup page - Renders the form
@app.route('/signup')
def signup_page():
    return render_template('signup.html')

# Signup logic - Handles form submission
@app.route('/signup_logic', methods=['POST'])
def signup_logic():
    users = load_users()
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('user_type')

    if not username or not email or not password or not user_type:
        return jsonify({"message": "All fields are required."}), 400

    if username in users:
        return jsonify({"message": "Username already exists."}), 409

    if initialize_firebase_app():
        try:
            # Create user in Firebase Auth
            firebase_user = auth.create_user(email=email, password=password, display_name=username)
            firebase_uid = firebase_user.uid

            # Hash local password (if keeping local store)
            hashed_password = generate_password_hash(password)

            # Save local mapping
            users[username] = {
                "email": email,
                "password": hashed_password,
                "user_type": user_type,
                "firebase_uid": firebase_uid
            }
            save_users(users)

            # Create custom token for client-side sign-in
            custom_token = auth.create_custom_token(firebase_uid)
            if isinstance(custom_token, bytes):
                custom_token = custom_token.decode('utf-8')

            return jsonify({
                "message": "Account created successfully!",
                "userType": user_type,
                "customToken": custom_token
            }), 201

        except exceptions.FirebaseError as e:
            print(f"Firebase Auth error during user creation: {e}")
            return jsonify({"message": "Firebase authentication error occurred."}), 500
        except Exception as e:
            print(f"General error during signup: {e}")
            return jsonify({"message": "An unexpected error occurred during signup."}), 500
    else:
        return jsonify({"message": "Firebase Admin SDK not initialized."}), 500


# Login page
@app.route('/login')
def login():
    return render_template('login.html')

# Login logic
@app.route('/login_logic', methods=['POST'])
def login_logic():
    users = load_users()
    data = request.json
    username = data.get('username')
    password = data.get('password')

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
        return jsonify({"message": "An unexpected error occurred during login."}), 500


@app.route('/artist-dashboard')
def artist_dashboard():
    return render_template('artist-dashboard.html')

@app.route('/privacy-policy.html')
def privacy_policy():
    return render_template('privacy-policy.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/faq.html')
def faq():
    return render_template('faq.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/terms-of-service.html')
def terms_of_service():
    return render_template('terms-of-service.html')

@app.route('/State-region.html')
def State_region():
    return render_template('State-region.html')

@app.route('/Himachal.html')
def Himachal():
    return render_template('Himachal.html')

@app.route('/Rajasthan.html')
def Rajasthan():
    return render_template('Rajasthan.html')

@app.route('/MP.html')
def MP():
    return render_template('MP.html')

@app.route('/UP.html')
def UP():
    return render_template('UP.html')
    
@app.route('/J_K.html')
def J_K():
    return render_template('J_K.html')

@app.route('/Odisha.html')
def Odisha():
    return render_template('Odisha.html')

@app.route('/West-Bengal.html')
def West_Bengal():
    return render_template('West-Bengal.html')

@app.route('/Assam.html')
def Assam():
    return render_template('Assam.html')

@app.route('/Tamil-Nadu.html')
def Tamil_Nadu():
    return render_template('Tamil-Nadu.html')

@app.route('/kerala.html')
def kerala():
    return render_template('kerala.html')

@app.route('/karnataka.html')
def karnataka():
    return render_template('karnataka.html')

@app.route('/Gujarat.html')
def Gujarat():
    return render_template('Gujarat.html')

@app.route('/bharatnatyam.html')
def bharatnatyam():
    return render_template('bharatnatyam.html')

@app.route('/thanjavur')
def thanjavur():
    return render_template('thanjavur.html')

@app.route('/chola')
def chola():
    return render_template('chola.html')

@app.route('/kanchi')
def kanchi():
    return render_template('kanchi.html')

@app.route('/Swood')
def Swood():
    return render_template('Swood.html')

@app.route('/chikankari')
def chikankari():
    return render_template('chikankari.html')

@app.route('/Fglass')
def Fglass():
    return render_template('Fglass.html')

@app.route('/bsilk')
def bsilk():
    return render_template('bsilk.html')

@app.route('/Kantha')
def Kantha():
    return render_template('Kantha.html')

@app.route('/TerracottaWB')
def TerracottaWB():
    return render_template('TerracottaWB.html')

@app.route('/Kalighat')
def Kalighat():
    return render_template('Kalighat.html')

@app.route('/Chhau')
def Chhau():
    return render_template('Chhau.html')

@app.route('/login-events')
def login_events():
    return render_template('login-events.html')

@app.route('/login-register')
def login_register():
    return render_template('login-register.html')

if __name__ == '__main__':
    initialize_firebase_app()
    app.run(debug=True)
