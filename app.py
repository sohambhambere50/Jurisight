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

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         # If user uppload a file
#         if 'file' in request.files:
#             file = request.files['file']
            
#             if file and allowed_file(file.filename):
#                 filename = secure_filename(file.filename)
#                 filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#                 file.save(filepath)

#                 clauses = extract_clauses(filepath)
#                 summary, full_details = summarize_text(clauses)

#                 return render_template("result.html", full_details = full_details, clauses = clauses,  summary = summary)
        
#         user_text = request.form.get("user_text")
#         if user_text.strip():
#             clauses = extract_clauses(user_text, is_file = False)
#             summary, full_details = summarize_text(clauses)

#             return render_template("result.html", full_details = full_details, clauses= clauses, summary = summary)
    
#     return render_template("index.html")
 

@app.route("/", methods=["GET", "POST"])
def process_file_prompt():
    if request.method == "POST":
        file = request.files.get('file')
        user_prompt = request.form.get('user_prompt')
        
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Extract clauses/text from file
            extracted_text = extract_clauses(filepath)

            # Combine user prompt with extracted text as input prompt for model
            combined_prompt = f"""
                You are a legal document analyst specialized in extracting and explaining clauses. 

                Your task is to read the given document text and perform the following:

                1. Extract ONLY the distinct clauses in the document. A clause is a separate, meaningful contractual point or condition.
                2. For each extracted clause, write a clear and simple explanation understandable by someone without legal expertise.
                3. Ignore formatting issues, random letters, headers, footers, and any unrelated text.
                4. Present the output as a numbered list where each item has:
                    - The clause text exactly as in the document
                    - Followed immediately by its simple explanation in plain language
                5. Do NOT combine multiple clauses into one point.
                6. Keep the explanations concise but informative.

                Now, consider the user's specific instructions below and apply them while performing the task:

                User's additional instructions: {user_prompt}

                Here is the document text for analysis:
                {extracted_text}

             """

            # Call your summarization function with combined prompt
            summary, full_details = summarize_text(combined_prompt)

            # Pass results and optionally extracted clauses to template
            return render_template(
                "result.html",
                summary=summary,
                full_details=full_details,
                clauses=extracted_text if isinstance(extracted_text, list) else extracted_text.split('\n')
            )
    # For GET requests, simply render the upload+prompt form page
    return render_template("upload_prompt.html")



@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)