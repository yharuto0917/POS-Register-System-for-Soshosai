import os
from firebase_functions import https_fn

def getLineAccessToken():
    key = os.environ.get("LINE_ACCESS_TOKEN")
    return key