import re
from openai import OpenAI 
from config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

def summarize_text(final_prompt: str):
    """
    Takes a fully constructed prompt (from app.py) and queries the model.
    Returns cleaned output and raw text.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a legal document clause summarizer."},
            {"role": "user", "content": final_prompt}
        ],
        temperature=0.3
    )

    raw_output = response.choices[0].message.content.strip()

    # --- Clean formatting (ensure consistent numbering) ---
    def clean_summary(text):
        points = re.split(r'\d+\.\s', text)  # split at numbered list
        points = [p.strip() for p in points if p.strip()]
        cleaned_lines = [f"{i}. {point}" for i, point in enumerate(points, 1)]
        return "\n".join(cleaned_lines)

    cleaned_output = clean_summary(raw_output)
    return cleaned_output, raw_output
