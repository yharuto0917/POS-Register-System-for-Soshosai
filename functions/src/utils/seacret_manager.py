import os
from firebase_functions import https_fn

@https_fn.on_request(secret=["GEMINI_API_KEY"])
def getGeminiApiKey(req: https_fn.Request) -> https_fn.Response:
    return https_fn.Response(os.environ["GEMINI_API_KEY"])