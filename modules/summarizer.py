import re
import os
from openai import OpenAI 
from config import Config

# client = Config.OPENAI_API_KEY
client = OpenAI(api_key=Config.OPENAI_API_KEY)

def summarize_text(clauses):
    summary_prompt = f"""
        You are a legal document analyzer. Read the following text and extract ONLY the essential points.

        Your job:
        - Identify: Parties involved, Document type, Financial amounts, and Key obligations.
        - Ignore: formatting artifacts, random letters, irrelevant text.

        Strict Output Rules:
        - Output only a NEW LINE for each numbered point. Do NOT include more than ONE POINT per line under any circumstance.
        - Do NOT use paragraphs, just exactly one point per line, numbered 1., 2., 3., etc.
        - Do NOT skip numbering, even if information is missing (write 'Not specified' if absent).

        WARNING: If you do not format as instructed, you will be penalized.

        Final Output Example:
        1. Parties Involved: <text here>
        2. Document Type: <text here>
        3. Financial Amounts: <text here>
        4. Key Obligations: <text here>

        Text to analyze:
        {clauses}
    """

    summary_response = client.chat.completions.create(
        model= "gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a legal document clause summarizer."},
            {"role": "user", "content": summary_prompt}
        ],
        temperature=0.3
    )

    raw_summary = summary_response.choices[0].message.content.strip()

    def clean_summary(response_text):
        # Split text on any numbering pattern like "1. ", "2. ", "10. ", etc.
        points = re.split(r'\d+\.\s', response_text)
        # Remove empty entries after splitting
        points = [p.strip() for p in points if p.strip()]
        # Re-number sequentially from 1
        cleaned_lines = [f"{i}. {point}" for i, point in enumerate(points, 1)]
        return "\n".join(cleaned_lines)
    
    key_points = clean_summary(raw_summary)
    return key_points, clauses

