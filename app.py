from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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
from modules.document_reader import extract_text
from modules.chatbot import answer_query
from config import Config
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

def allowed_file(filename):
    return '.' in filename and filename.resplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=["GET", "POST"])
def home():
    # Renders the main page of the application.
    return render_template('login.html')

# # Database creation for Login and Signup page
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv("SECRET_KEY")  #need to create the secret key

# # Mail config (example with Gmail SMTP). Replace with env vars in production
MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ('true','1','t')
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', os.getenv('MAIL_USERNAME'))

# # To test the email configuration is working correctly or not 
# print("MAIL_USERNAME =", MAIL_USERNAME)
# print("MAIL_SERVER =", MAIL_SERVER)
# print("MAIL_PORT =", MAIL_PORT)

mail.init_app(app) #Initialization of mail 

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {"timeout": 30}  # wait up to 30 seconds if DB is locked
}
db.init_app(app) #Initialization of User database

with app.app_context():
    db.create_all()

# Route for signup.html page
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

# Routes for login.html page
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

# Route to open chatbot.html page
@app.route('/chatbot',methods=['GET'])
def chatbot_page():
    return render_template("chatbot.html")

# Route to process the user query
@app.route('/chatbot', methods=['POST'])
def chatbot_api():
    user_message = request.form.get("user_message","").strip()
    uploaded_file = request.files.get("file")

    document_text = ""
    if uploaded_file and allowed_file(uploaded_file.filename):
        filename = secure_filename(uploaded_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(filepath)
        document_text = extract_text(filepath)
        # os.remove(filepath)

    if not user_message and not document_text:
        return jsonify({"reply" : "Please enter query or upload a documnet."})
    
    reply = answer_query(user_message, document_text if document_text else None)
    return jsonify({"reply" : reply})
    
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# @app.route("/", methods=["GET", "POST"])
# def process_file_prompt():
#     if request.method == "POST":
#         file = request.files.get('file')
#         user_prompt = request.form.get('user_prompt')
        
#         if file and file.filename != '' and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)

#             # Extract clauses/text from file
#             extracted_text = extract_clauses(filepath)

#             # Build one single prompt
#             combined_prompt = f"""
#             You are a legal document analyst specialized in extracting and explaining clauses.

#             Your task is to read the given document text and perform the following:

#             1. Extract ONLY the distinct clauses in the document. 
#             2. Provide a plain-language explanation for each clause. 
#             3. Ignore irrelevant or noisy text. 
#             4. Present the output as a numbered list (Clause + Explanation).
#             5. Do not merge multiple clauses into one.

#             User additional instructions: {user_prompt}

#             Document text for analysis:
#             {extracted_text}
#             """

#             # Call summarizer with only one prepared prompt
#             summary, full_details = summarize_text(combined_prompt)

#             return render_template(
#                 "result.html",
#                 summary=summary,
#                 full_details=full_details,
#                 clauses=extracted_text if isinstance(extracted_text, list) else extracted_text.split('\n')
#             )

#     # Default GET route
#     return render_template("index.html")





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
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True) # Run the Flask application in debug mode