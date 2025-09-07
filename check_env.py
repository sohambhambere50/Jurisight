import os
from dotenv import load_dotenv

# Load .env from current folder
load_dotenv()

print("OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))
print("MODEL_NAME =", os.getenv("MODEL_NAME"))
