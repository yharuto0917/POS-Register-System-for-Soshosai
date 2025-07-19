# import src.api.api_gemini as getGeminiApiKey

"""
引数:
{
    "contents":{
        "model_name": "Gemini model name(ex: gemini-2.5-flash)",
        "prompt": "prompt for gemini",
        "materials": "materials for gemini"
    }
}
"""

def geminiAnalyze(contents):
    print(f"geminiAnalyze is called with: {contents}")
    return {"status": "success", "message": "Gemini analyzed."}