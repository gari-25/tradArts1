from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import json, os
import firebase_admin
from firebase_admin import credentials, auth, exceptions

app = Flask(__name__)
# IMPORTANT: Set a strong secret key for session management in production
# app.secret_key = os.urandom(24) # Use this line in production
app.secret_key = 'super_secret_key_dev' # For development only, change for production!

users_file = 'users.json'

# --- Firebase Admin SDK Initialization ---
# This approach is more robust for Flask's reloader:
# It tries to get the default app; if it doesn't exist, it initializes it.
firebase_initialized = False
try:
    firebase_app_instance = firebase_admin.get_app()
    firebase_initialized = True
    print("Firebase Admin SDK already initialized.")
except ValueError: # This error is raised if the default app does not exist
    try:
        # IMPORTANT: Replace "serviceAccountKey.json" with the actual path
        # to your downloaded Firebase service account key JSON file.
        # Ensure this file is in the same directory as app.py, or provide its full path.
        cred = credentials.Certificate("serviceAccountKey.json") # Assuming it's in the same directory
        firebase_admin.initialize_app(cred)
        firebase_initialized = True
        print("Firebase Admin SDK initialized successfully.")
    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {e}")
        firebase_initialized = False
except Exception as e: # Catch any other unexpected errors during get_app()
    print(f"Unexpected error when checking Firebase app instance: {e}")
    firebase_initialized = False


# --- User Management Functions (Load/Save from JSON) ---
def load_users():
    """Loads user data from the JSON file."""
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Saves user data to the JSON file."""
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=4)

# --- Flask Routes ---
@app.route('/')
def home():
    """Redirects to the signup page."""
    return redirect(url_for('signup_page'))

@app.route('/signup')
def signup_page():
    """Renders the signup HTML page."""
    return render_template('signup.html')

@app.route('/login')
def login_page():
    """Renders the login HTML page."""
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Renders the general user dashboard HTML page."""
    return render_template('dashboard.html')

@app.route('/artist-dashboard')
def artist_dashboard_route():
    """Renders the artist dashboard HTML page."""
    return render_template('artist-dashboard.html')

@app.route('/login-events')
def login_events_page():
    """Renders the events HTML page."""
    return render_template('login-events.html')

@app.route('/login-register')
def login_register_page():
    """Renders the event registration HTML page."""
    return render_template('login-register.html')

# --- Signup logic ---
@app.route('/signup', methods=['POST'])
def signup():
    """Handles user signup, creates Firebase Auth user, and issues custom token."""
    # Ensure Firebase Admin SDK is initialized before proceeding
    if not firebase_initialized:
        print("Firebase Admin SDK not initialized. Cannot process signup.")
        return jsonify({"message": "Server configuration error. Please try again later."}), 500

    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    user_type = data.get("user_type")

    users = load_users()

    # 1. Check if username exists in your local JSON
    if username in users:
        return jsonify({"message": "Username already exists."}), 409

    # 2. Check if email exists in Firebase Authentication
    try:
        auth.get_user_by_email(email)
        # If get_user_by_email succeeds, it means the email is already registered in Firebase Auth.
        return jsonify({"message": "Email already registered in Firebase."}), 409
    except exceptions.FirebaseError as e:
        # --- DEBUGGING LINE (now fixed condition) ---
        print(f"DEBUG: FirebaseError code during email check: '{e.code}'")
        # --- END DEBUGGING LINE ---

        # If the error is 'NOT_FOUND', it means the email is available, so we proceed to create.
        # This is the crucial change: 'auth/user-not-found' is actually 'NOT_FOUND'
        if e.code == 'NOT_FOUND': # <--- CHANGED THIS LINE
            pass # Email is available, continue to create user
        else:
            # Any other FirebaseError is an actual server-side issue.
            print(f"Firebase Auth error checking email: {e}")
            return jsonify({"message": f"Firebase Auth error: {e.code}"}), 500
    except Exception as e:
        # Catch any other unexpected errors during the email check
        print(f"General error during email check: {e}")
        return jsonify({"message": "An unexpected error occurred during email check."}), 500

    # 3. If email is not registered in Firebase Auth, create the user
    try:
        firebase_user = auth.create_user(email=email, password=password)
        firebase_uid = firebase_user.uid
        print(f"Firebase Auth user created with UID: {firebase_uid}")

        # 4. Save user details to your local JSON (users.json)
        # IMPORTANT: In a real application, NEVER store plain passwords!
        # You should hash passwords before saving them, e.g., using bcrypt.
        # For this demo, Firebase handles the actual password storage securely for auth.
        users[username] = {
            "email": email,
            "password": password, # This is for local JSON check only
            "user_type": user_type,
            "firebase_uid": firebase_uid # Store Firebase UID
        }
        save_users(users)

        # 5. Create a custom token for the newly created user
        custom_token = auth.create_custom_token(firebase_uid).decode('utf-8')
        print(f"Custom token created for {username}.")

        return jsonify({
            "message": "Signup successful!",
            "customToken": custom_token,
            "userType": user_type, # Send user type back to client
            "email": email # Send email back for client-side Firebase Auth
        }), 201

    except exceptions.FirebaseError as e:
        print(f"Firebase Auth error during user creation: {e}")
        return jsonify({"message": f"Firebase Auth user creation failed: {e.code}"}), 500
    except Exception as e:
        print(f"General error during signup: {e}")
        return jsonify({"message": "An unexpected error occurred during signup."}), 500


# --- Login logic ---
@app.route('/login', methods=['POST'])
def login():
    """Handles user login, verifies credentials, and issues custom token."""
    # Ensure Firebase Admin SDK is initialized before proceeding
    if not firebase_initialized:
        print("Firebase Admin SDK not initialized. Cannot process login.")
        return jsonify({"message": "Server configuration error. Please try again later."}), 500

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    users = load_users()

    # 1. Check if username and password match in local JSON
    if username not in users or users[username]["password"] != password:
        return jsonify({"message": "Invalid username or password."}), 401

    user_data = users[username]
    email = user_data["email"]
    user_type = user_data["user_type"]
    firebase_uid = user_data.get("firebase_uid") # Get Firebase UID from JSON

    # 2. If Firebase UID is missing in your local JSON, try to get it from Firebase Auth by email
    # This can happen if a user was created before Firebase UID was stored in users.json
    if not firebase_uid:
        try:
            firebase_user = auth.get_user_by_email(email)
            firebase_uid = firebase_user.uid
            # Update users.json with the firebase_uid if it was missing
            user_data["firebase_uid"] = firebase_uid
            save_users(users)
        except exceptions.FirebaseError as e:
            print(f"Firebase Auth error getting user by email during login: {e}")
            return jsonify({"message": "Firebase user not found or error occurred."}), 401
        except Exception as e:
            print(f"General error during login UID lookup: {e}")
            return jsonify({"message": "An unexpected error occurred during login."}), 500

    # 3. Create a custom token for the authenticated user
    try:
        custom_token = auth.create_custom_token(firebase_uid).decode('utf-8')
        print(f"Custom token created for {username} (UID: {firebase_uid}).")

        return jsonify({
            "message": "Login successful!",
            "customToken": custom_token,
            "userType": user_type
        }), 200

    except exceptions.FirebaseError as e:
        print(f"Firebase Auth error during custom token creation: {e}")
        return jsonify({"message": f"Firebase Auth error: {e.code}"}), 500
    except Exception as e:
        print(f"General error during login: {e}")
        return jsonify({"message": "An unexpected error occurred during login."}), 500


if __name__ == '__main__':
    # This ensures the Flask development server reloads correctly.
    # For production, a WSGI server (like Gunicorn) will manage this.
    app.run(debug=True)
