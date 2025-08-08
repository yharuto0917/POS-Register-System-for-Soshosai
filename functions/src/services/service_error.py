BROADCAST_URL = "https://api.line.me/v2/bot/message/broadcast"

"""
引数:
{
    "contents":{
        "message": "エラーログの内容",
        "storeName": "店舗名",
        "function_name": "エラーが発生した関数名"
    }
}
"""

import requests
from src.api.api_line import getLineAccessToken

def sendErrorLog(contents):
    # ラインアクセストークンを取得
    line_access_token = getLineAccessToken()

    headers = {
        'Authorization': f'Bearer {line_access_token}',
        'Content-Type': 'application/json'
    }

    message = setMessage(contents)

    payload = {
        'messages':[
            {
                'type': 'text',
                'text': message
            }
        ]
    }

    # ラインメッセージを送信
    try:
        response = requests.post(
            BROADCAST_URL,
            headers=headers,
            json=payload
        )
        return {'status': 'success', 'message': 'Error log sent.'}
    except Exception as e:
        print(f"sendErrorLogの実行中にエラーが発生しました: {e}")
        return {"status": "error", "message": f"sendErrorLogの実行中にエラーが発生しました: {e}"}


def setMessage(contents):
    message = f"POSシステムfor蒼翔祭が{contents['storeName']}でエラーが発生しました。\n"
    message += f"エラー関数名: {contents['function_name']}\n"
    message += f"エラーログ: {contents['message']}"
    return message