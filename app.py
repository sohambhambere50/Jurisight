from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session
from flask_migrate import Migrate
from extension import mail
from utils import send_verification_email
from werkzeug.utils import secure_filename 
import os
import secrets
import string
from datetime import datetime
from dotenv import load_dotenv
from modules.clause_extractor import extract_clauses
from modules.summarizer import summarize_text
from config import Config
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    # Renders the main page of the application.
    return render_template('login.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')


# Database creation for Login and Signup page
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv("SECRET_KEY")  #need to create the secret key



# Mail config (example with Gmail SMTP). Replace with env vars in production
MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ('true','1','t')
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', os.getenv('MAIL_USERNAME'))

print("MAIL_USERNAME =", MAIL_USERNAME)
print("MAIL_SERVER =", MAIL_SERVER)
print("MAIL_PORT =", MAIL_PORT)

mail.init_app(app) #Initialization of mail 

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {"timeout": 30}  # wait up to 30 seconds if DB is locked
}
db.init_app(app) #Initialization of User database

with app.app_context():
    db.create_all()

# Route for Signup page
@app.route('/signup', methods=['GET','POST'])
def signup():
    print("Signup page is running with:", request.method)
    if request.method == 'GET':        
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        # check if user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or Email already existed!")
            return redirect(url_for('signup'))
        
        # Create new user with hashed password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username = username, email = email, password = hashed_password)

        # # Generate 6 digit verification code 
        code = ''.join(secrets.choice(string.digits) for _ in range(6))

        # # Store code hashed + sent time
        new_user.verification_code_hash = generate_password_hash(code)
        new_user.verification_sent_at = datetime.utcnow()
        new_user.email_confirmed = False

        # Send verification email 
        print("Email is about to send..")
        send_verification_email(new_user, code) 

        db.session.add(new_user)
        db.session.commit()

        session['pending_user_id'] = new_user.id

        flash("Signup successful! A verification code has been sent to email. Please verify.")
        return redirect(url_for('verify'))
        # return redirect(url_for('login'))


    return render_template('signup.html')

# Routes for login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("Login Successful!")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password")

    return render_template('login.html')

# # Verification Route 
@app.route('/verify')
def verify():
    return render_template('verify.html')

# # If the login is not there then return to home page else open the landing page after login
# @app.route('/index')
# def index():
#     if 'user_id' not in session:
#         flash("Please login first!")
#         return redirect(url_for('login'))
#     return "Welcome to website!"

# # Logout Route
# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     return redirect('landing_page')

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)