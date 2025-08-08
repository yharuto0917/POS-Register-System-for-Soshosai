import os

def getLineAccessToken():
    key = os.environ.get("LINE_ACCESS_TOKEN")
    return key