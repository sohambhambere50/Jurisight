from flask import Flask, render_template, request
from werkzeug.utils import secure_filename 
import os
from modules.clause_extractor import extract_clauses
from modules.summarizer import summarize_text
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # If user uppload a file
        if 'file' in request.files:
            file = request.files['file']
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                clauses = extract_clauses(filepath)
                summary, full_details = summarize_text(clauses)

                return render_template("result.html", full_details = full_details, summary = summary)
        
        user_text = request.form.get("user_text")
        if user_text.strip():
            clauses = extract_clauses(user_text, is_file = False)
            summary, full_details = summarize_text(clauses)

            return render_template("result.html", full_details = full_details, summary = summary)
    
    return render_template("index.html")

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)