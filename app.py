from flask import Flask, render_template, request
from werkzeug.utils import secure_filename 
import os
from modules.clause_extractor import extract_clauses
from modules.summarizer import summarize_text
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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

            # Build one single prompt
            combined_prompt = f"""
            You are a legal document analyst specialized in extracting and explaining clauses.

            Your task is to read the given document text and perform the following:

            1. Extract ONLY the distinct clauses in the document. 
            2. Provide a plain-language explanation for each clause. 
            3. Ignore irrelevant or noisy text. 
            4. Present the output as a numbered list (Clause + Explanation).
            5. Do not merge multiple clauses into one.

            User additional instructions: {user_prompt}

            Document text for analysis:
            {extracted_text}
            """

            # Call summarizer with only one prepared prompt
            summary, full_details = summarize_text(combined_prompt)

            return render_template(
                "result.html",
                summary=summary,
                full_details=full_details,
                clauses=extracted_text if isinstance(extracted_text, list) else extracted_text.split('\n')
            )

    # Default GET route
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
