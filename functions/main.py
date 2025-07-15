from firebase_functions import https_fn
from firebase_admin import initialize_app

initialize_app()

@https_fn.onCall()
def on_call_backend(req: https_fn.CallableContext) -> https_fn.Response:

    if(req.data is None):
        print("リクエストデータが存在しません[req.data is None in functions/main.py]")
        raise https_fn.HttpsError(
            code = https_fn.HttpsError.INVALID_ARGUMENT,
            message = "リクエストデータが存在しません[req.data is None in functions/main.py]"
        )

    function_name = req.data.get("function_name")

    if(function_name is None):
        print("function_nameが存在しません[function_name is None in functions/main.py]")
        raise https_fn.HttpsError(
            code = https_fn.HttpsError.INVALID_ARGUMENT,
            message = "function_nameが存在しません[function_name is None in functions/main.py]"
        )
    
    if(function_name == "sendErrorLog"):
        result = sedErroLog(req.data.contents)
        return https_fn.Response(result)
    elif(function_name == "geminiAnalyze"):
        result = geminiAnalyze(req.data.contents)
        return https_fn.Response(result)
    elif(function_name == "excuteGAS"):
        result = excuteGAS(req.data.contents)
        return https_fn.Response(result)
    else:
        print("function_nameが存在しません[function_name is None in functions/main.py]")
        raise https_fn.HttpsError(
            code = https_fn.HttpsError.INVALID_ARGUMENT,
            message = "function_nameが存在しません[function_name is None in functions/main.py]"
        )