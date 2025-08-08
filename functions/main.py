from firebase_functions import https_fn
from firebase_admin import initialize_app
from src.services.service_gemini import geminiAnalyze
from src.services.service_error import sendErrorLog
from src.services.service_gas import excuteGAS

initialize_app()

@https_fn.on_call(secrets=["GEMINI_API_KEY","LINE_ACCESS_TOKEN"])
def on_call_backend(req: https_fn.CallableRequest) -> any:

    if(req.data is None):
        raise https_fn.HttpsError(
            code = https_fn.FunctionsErrorCode.INVALID_ARGUMENT,
            message = "リクエストデータが存在しません[req.data is None in functions/main.py]"
        )
    
    if(req.data.get("function_name") is None):
        raise https_fn.HttpsError(
            code = https_fn.FunctionsErrorCode.INVALID_ARGUMENT,
            message = "function_nameが存在しません[function_name is None in functions/main.py]"
        )

    function_name = req.data.get("function_name")

    try:
        contents = req.data.get("contents")
    except Exception as e:
        raise https_fn.HttpsError(
            code = https_fn.FunctionsErrorCode.INTERNAL,
            message = f"contentsの取得中にエラーが発生しました: {e}"
        )
    
    if(function_name == "sendErrorLog"):
        try:
            result = sendErrorLog(contents)
            return result
        except Exception as e:
            raise https_fn.HttpsError(
                code = https_fn.FunctionsErrorCode.INTERNAL,
                message = f"sendErrorLog実行中にエラーが発生しました: {e}"
            )
    elif(function_name == "geminiAnalyze"):
        try:
            result = geminiAnalyze(contents)
            return result
        except Exception as e:
            raise https_fn.HttpsError(
                code = https_fn.FunctionsErrorCode.INTERNAL,
                message = f"geminiAnalyze実行中にエラーが発生しました: {e}"
            )
    elif(function_name == "excuteGAS"):
        try:
            result = excuteGAS(contents)
            return result
        except Exception as e:
            raise https_fn.HttpsError(
                code = https_fn.FunctionsErrorCode.INTERNAL,
                message = f"excuteGAS実行中にエラーが発生しました: {e}"
            )
    else:
        raise https_fn.HttpsError(
            code = https_fn.FunctionsErrorCode.INVALID_ARGUMENT,
            message=f"指定された関数名 '{function_name}' は存在しません。"
        )