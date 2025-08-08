import os

def getGeminiApiKey():
    key = os.environ.get("GEMINI_API_KEY")
    return key