from firebase_functions import https_fn
from firebase_admin import initialize_app
from src.services.service_gemini import geminiAnalyze

initialize_app()

@https_fn.on_call()
def on_call_backend(req: https_fn.CallableRequest) -> any:

    if(req.data is None):
        print("リクエストデータが存在しません[req.data is None in functions/main.py]")
        raise https_fn.HttpsError(
            code = https_fn.HttpsErrorCode.INVALID_ARGUMENT,
            message = "リクエストデータが存在しません[req.data is None in functions/main.py]"
        )

    function_name = req.data.get("function_name")
    print(f"function_name: {function_name}")

    if(function_name is None):
        print("function_nameが存在しません[function_name is None in functions/main.py]")
        raise https_fn.HttpsError(
            code = https_fn.HttpsErrorCode.INVALID_ARGUMENT,
            message = "function_nameが存在しません[function_name is None in functions/main.py]"
        )
    
    contents = req.data.get("contents")
    
    if(function_name == "sendErrorLog"):
        result = sedErroLog(contents)
        return https_fn.Response(result)
    elif(function_name == "geminiAnalyze"):
        return geminiAnalyze(contents)
    elif(function_name == "excuteGAS"):
        result = excuteGAS(contents)
        return https_fn.Response(result)
    else:
        print(f"指定された関数名 '{function_name}' は存在しません。")
        raise https_fn.HttpsError(
            code = https_fn.HttpsErrorCode.INVALID_ARGUMENT,
            message=f"指定された関数名 '{function_name}' は存在しません。"
        )