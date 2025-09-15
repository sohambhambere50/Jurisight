from openai import OpenAI
from config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

def ask_openai(prompt):
    """
    Send a query to OpenAI and return the response.
    Supports Hindi + English automatically.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """
                You are a highly knowledgeable and helpful Legal AI Assistant specializing in **Indian Laws and the Constitution of India**.
                Always answer queries **only in the context of Indian law**, providing clear references to IPC (Indian Penal Code), CrPC (Code of Criminal Procedure), or other relevant acts.

                Formatting Rules:
                - Always present answers in a structured, ordered list (1., 2., 3.…).
                - Each point must start on a new line.
                - Highlight important terms using **bold**.
                - Use limited emojis like ⚖️, ✅, 📌.
                - If exact law sections are available, mention them (e.g., Section 302 IPC).
                - If the question is vague, provide Indian legal perspective and mention "consult a professional for detailed advice".

                Always ensure answers are clear, structured, and directly relevant to Indian law.
            """},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=600
    )
    return response.choices[0].message.content.strip()

def answer_query(user_query, document_text=None):
    """
    If document is provided, combine query + doc context.
    Otherwise, just answer the query directly.
    """
    if document_text:
        combined_prompt = f"""
        The user has uploaded a legal document. Use the text below as context.

        Document:
        {document_text[:6000]}  # keep input safe from token overflow

        User's Question:
        {user_query}

        Answer in simple human language (Hindi or English as per user query) and provide response in point wise manner and bold the important word.
        """
        return ask_openai(combined_prompt)
    else:
        return ask_openai(user_query)
