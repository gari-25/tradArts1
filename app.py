from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin.auth import UserNotFoundError

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
            cred = credentials.Certificate("serviceAccountKey.json")
            
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK initialized successfully.")
        return True
    except FileNotFoundError:
        print("Error: 'serviceAccountKey.json' not found. Ensure it is in the same directory or FIREBASE_ADMIN_CREDENTIALS environment variable is set.")
        return False
    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {e}")
        return False

# --- User Data Helpers ---
def load_users():
    """Loads user data from the JSON file."""
    if not os.path.exists(users_file):
        with open(users_file, 'w') as f:
            json.dump({}, f)
        return {}
    with open(users_file, 'r') as f:
        return json.load(f)

def save_users(users):
    """Saves user data to the JSON file."""
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=4)

# --- Authentication Routes ---
@app.route('/login', methods=['GET'])
def login():
    """Renders the login page."""
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    """Handles user login and creates a custom token."""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    users = load_users()
    if username not in users or not check_password_hash(users[username]["password"], password):
        return jsonify({"message": "Invalid username or password."}), 401

    user_data = users[username]
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
        return jsonify({"message": "Error creating custom token."}), 500

@app.route('/signup', methods=['GET'])
def signup():
    """Renders the registration page."""
    return render_template('register.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    """Handles user registration and creates a Firebase user."""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    user_type = data.get('user_type')

    users = load_users()
    if username in users:
        return jsonify({"message": "Username already exists."}), 409
    
    try:
        # Create user in Firebase
        firebase_user = auth.create_user(
            email=email,
            password=password
        )
        firebase_uid = firebase_user.uid
        
        # Save user data locally
        users[username] = {
            "password": generate_password_hash(password),
            "email": email,
            "user_type": user_type,
            "firebase_uid": firebase_uid
        }
        save_users(users)

        return jsonify({"message": "User created successfully!", "uid": firebase_uid}), 201
    except Exception as e:
        print(f"Error creating Firebase user: {e}")
        return jsonify({"message": "Error creating user."}), 500


# --- Routes for all HTML pages ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/State-region')
def State_region():
    return render_template('State-region.html')

@app.route('/BMP')
def BMP():
    return render_template('BMP.html')

@app.route('/Sattriya')
def Sattriya():
    return render_template('Sattriya.html')

@app.route('/Majuli')
def Majuli():
    return render_template('Majuli.html')

@app.route('/Muga')
def Muga():
    return render_template('Muga.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/terms-of-service')
def terms_of_service():
    return render_template('terms-of-service.html')

@app.route('/warli')
def warli():
    return render_template('warli.html')

@app.route('/vastra')
def vastra():
    return render_template('vastra.html')

@app.route('/madhubani')
def madhubani():
    return render_template('madhubani.html')

@app.route('/fabric')
def fabric():
    return render_template('fabric.html')

@app.route('/string')
def string():
    return render_template('string.html')

@app.route('/clay')
def clay():
    return render_template('clay.html')

@app.route('/Rogan')
def Rogan():
    return render_template('Rogan.html')

@app.route('/Beadwork')
def Beadwork():
    return render_template('Beadwork.html')

@app.route('/Lippan')
def Lippan():
    return render_template('Lippan.html')

@app.route('/Wood_Craft')
def Wood_Craft():
    return render_template('Wood Craft.html')

@app.route('/Chamba')
def Chamba():
    return render_template('Chamba.html')

@app.route('/pahari')
def pahari():
    return render_template('pahari.html')

@app.route('/hjewellery')
def hjewellery():
    return render_template('hjewellery.html')

@app.route('/bamboo')
def bamboo():
    return render_template('bamboo.html')

@app.route('/kceiling')
def kceiling():
    return render_template('kceiling.html')

@app.route('/Papier_Mâché')
def Papier_Mâché():
    return render_template('Papier-Mâché.html')

@app.route('/Namda')
def Namda():
    return render_template('Namda.html')

@app.route('/wicker')
def wicker():
    return render_template('wicker.html')

@app.route('/kinnal')
def kinnal():
    return render_template('kinnal.html')

@app.route('/bidri')
def bidri():
    return render_template('bidri.html')

@app.route('/mysore')
def mysore():
    return render_template('mysore.html')

@app.route('/ilkal')
def ilkal():
    return render_template('ilkal.html')

@app.route('/kathakali')
def kathakali():
    return render_template('kathakali.html')

@app.route('/aranmula')
def aranmula():
    return render_template('aranmula.html')

@app.route('/coir')
def coir():
    return render_template('coir.html')

@app.route('/mural')
def mural():
    return render_template('mural.html')

@app.route('/Stone')
def Stone():
    return render_template('Stone.html')

@app.route('/Terracotta')
def Terracotta():
    return render_template('Terracotta.html')

@app.route('/Gond')
def Gond():
    return render_template('Gond.html')

@app.route('/Chanderi')
def Chanderi():
    return render_template('Chanderi.html')

@app.route('/Gotipua')
def Gotipua():
    return render_template('Gotipua.html')

@app.route('/Ikat_Weaving')
def Ikat_Weaving():
    return render_template('Ikat Weaving.html')

@app.route('/dhokra')
def dhokra():
    return render_template('dhokra.html')

@app.route('/Pattachitra')
def Pattachitra():
    return render_template('Pattachitra.html')

@app.route('/Kalbelia')
def Kalbelia():
    return render_template('Kalbelia.html')

@app.route('/Pichwai')
def Pichwai():
    return render_template('Pichwai.html')

@app.route('/Lakh_Bangles')
def Lakh_Bangles():
    return render_template('Lakh Bangles.html')

@app.route('/Puppetry')
def Puppetry():
    return render_template('Puppetry.html')

@app.route('/J_K')
def J_K():
    return render_template('J&K.html')

@app.route('/Assam')
def Assam():
    return render_template('Assam.html')

@app.route('/kerala')
def kerala():
    return render_template('kerala.html')

@app.route('/West_Bengal')
def West_Bengal():
    return render_template('West Bengal.html')

@app.route('/karnataka')
def karnataka():
    return render_template('karnataka.html')

@app.route('/UP')
def UP():
    return render_template('UP.html')

@app.route('/Odisha')
def Odisha():
    return render_template('Odisha.html')

@app.route('/Tamil_Nadu')
def Tamil_Nadu():
    return render_template('Tamil-Nadu.html')

@app.route('/Himachal')
def Himachal():
    return render_template('Himachal.html')

@app.route('/Rajasthan')
def Rajasthan():
    return render_template('Rajasthan.html')

@app.route('/MP')
def MP():
    return render_template('MP.html')

@app.route('/Gujarat')
def Gujarat():
    return render_template('Gujarat.html')

@app.route('/kalakosh_events')
def kalakosh_events():
    return render_template('kalakosh_events.html')

@app.route('/bharatnatyam')
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
def login_events():
    return render_template('login-register.html')

@app.route('/artist-dashboard')
def artist_dashboard():
    return render_template('artist-dashboard.html')

# --- Main Execution Block ---
if __name__ == '__main__':
    # Initialize Firebase Admin SDK
    if not initialize_firebase_app():
        print("Exiting due to Firebase initialization error.")
    else:
        # This ensures the Flask development server reloads correctly.
        app.run(debug=True, use_reloader=False)

