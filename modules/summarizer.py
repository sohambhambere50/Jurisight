import os
from openai import OpenAI 
from config import Config

# client = Config.OPENAI_API_KEY
client = OpenAI(api_key=Config.OPENAI_API_KEY)

def summarize_text(clauses):
    summary_prompt = f""" 
    From the following legal document text, extract ONLY the essential key points in clear, concise bullet points and add new line after every new point.

    Must include:
    - Parties involved
    - Document type
    - Financial amounts
    - Key obligations
    
    Ignore:
    - Fornatting artifacts
    -Random letters
    - Irrelevent text

    OUTPUT FORMAT (follow exactly):
    1. <First point>
    2. <Second point>
    3. <Third point>
    Text:
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

    key_points = summary_response.choices[0].message.content.strip()

    return key_points, clauses

