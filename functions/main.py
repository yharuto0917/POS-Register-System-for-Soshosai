from firebase_functions import https_fn
from firebase_admin import initialize_app
from src.services.service_gemini import geminiAnalyze
from src.services.service_error import sendErrorLog
from src.services.service_gas import excuteGAS

initialize_app()

@https_fn.on_call()
def on_call_backend(req: https_fn.CallableRequest) -> any:

    if(req.data is None):
        raise https_fn.HttpsError(
            code = https_fn.HttpsErrorCode.INVALID_ARGUMENT,
            message = "リクエストデータが存在しません[req.data is None in functions/main.py]"
        )
    
    if(req.data.get("function_name") is None):
        raise https_fn.HttpsError(
            code = https_fn.HttpsErrorCode.INVALID_ARGUMENT,
            message = "function_nameが存在しません[function_name is None in functions/main.py]"
        )

    function_name = req.data.get("function_name")

    try:
        contents = req.data.get("contents")
    except Exception as e:
        raise https_fn.HttpsError(
            code = https_fn.HttpsErrorCode.INTERNAL,
            message = f"contentsの取得中にエラーが発生しました: {e}"
        )
    
    if(function_name == "sendErrorLog"):
        result = sendErrorLog(contents)
        return result
    elif(function_name == "geminiAnalyze"):
        result = geminiAnalyze(contents)
        return result
    elif(function_name == "excuteGAS"):
        result = excuteGAS(contents, function_name)
        return result
    else:
        raise https_fn.HttpsError(
            code = https_fn.HttpsErrorCode.INVALID_ARGUMENT,
            message=f"指定された関数名 '{function_name}' は存在しません。"
        )