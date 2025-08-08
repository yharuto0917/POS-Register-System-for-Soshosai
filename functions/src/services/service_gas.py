import requests
import json

"""
引数:
{
    "function_name": "excuteGAS",
    "contents": {
        "process": "record",
        "orders": [以下のような注文データ]
    }
}

注文データ生成方法:
const sampleOrder1 = {
    id: "ord_" + Math.random().toString(36).substr(2, 9),
    storeId: "store-A",
    orderNumber: 101,
    items: [
      { productId: "prod-001", productName: "コーヒー豆", price: 1200, quantity: 2, subtotal: 2400 },
      { productId: "prod-002", productName: "マグカップ", price: 800, quantity: 1, subtotal: 800 }
    ],
    totalAmount: 3200,
    status: 'completed',
    orderDate: new Date()
  };

  const sampleOrder2 = {
    id: "ord_" + Math.random().toString(36).substr(2, 9),
    storeId: "store-B",
    orderNumber: 55,
    items: [
      { productId: "prod-003", productName: "ケーキセット", price: 1500, quantity: 1, subtotal: 1500 }
    ],
    totalAmount: 1500,
    status: 'pending',
    orderDate: new Date()
  };

  const sampleOrder3 = {
    id: "ord_" + Math.random().toString(36).substr(2, 9), // IDは新しくなる想定
    storeId: "store-B",
    orderNumber: 55, // 既存の注文番号
    items: [
        { productId: "prod-003", productName: "ケーキセット", price: 1500, quantity: 1, subtotal: 1500 },
        { productId: "prod-add", productName: "追加クッキー", price: 300, quantity: 1, subtotal: 300 }
    ],
    totalAmount: 1800,
    status: 'completed', // ステータスを更新
    orderDate: new Date()
  };

  // 4. 完了済み注文の上書き（スキップされるはず）
  const sampleOrder4 = {
    id: "ord_" + Math.random().toString(36).substr(2, 9),
    storeId: "store-A",
    orderNumber: 101, // 完了済みの注文番号
    items: [],
    totalAmount: 0,
    status: 'cancelled', // 変更しようと試みる
    orderDate: new Date()
  };

  const inf = {process: 'record',orders: [sampleOrder1,sampleOrder2,sampleOrder3,sampleOrder4]};
  return inf;
"""

def excuteGAS(contents):
    try:
        # 入力データの検証
        if not isinstance(contents, dict):
            raise ValueError("contentsはdict形式である必要があります")
        
        if not contents:
            raise ValueError("contentsが空です")

        # url無効化済み。テスト・本番用のurlを後に設定する
        url = 'https://script.google.com/xxxxxxxxx'
        
        if not url:
            raise ValueError("GAS URLが設定されていません")
        
        try:
            # GASへのPOSTリクエスト
            response = requests.post(url, json=contents, timeout=30)
            
            # HTTPステータスコードが 2xx (成功) でない場合に例外を発生させます
            response.raise_for_status()
            
            # レスポンスの内容を確認
            if not response.content:
                raise ValueError("GASからの応答が空です")
                
            try:
                result = response.json()
                return result
            except json.JSONDecodeError as e:
                # GASからの応答がJSON形式でない場合のエラーです
                print(f"Error: Failed to decode JSON from GAS. Response text: {response.text}")
                raise RuntimeError(f"GASからの応答がJSON形式ではありません: {e}")
                
        except requests.exceptions.Timeout:
            # タイムアウトエラーの場合
            print("Error: Request to GAS timed out")
            raise RuntimeError("GASへのリクエストがタイムアウトしました")
            
        except requests.exceptions.ConnectionError as e:
            # 接続エラーの場合
            print(f"Error: Connection to GAS failed: {e}")
            raise RuntimeError(f"GASへの接続に失敗しました: {e}")
            
        except requests.exceptions.HTTPError as e:
            # HTTPエラーの場合
            print(f"Error: HTTP error from GAS: {e}")
            raise RuntimeError(f"GASからHTTPエラーが返されました: {e}")
            
        except requests.exceptions.RequestException as e:
            # その他のリクエストエラーの場合
            print(f"Error: Request to GAS failed: {e}")
            raise RuntimeError(f"GASへのリクエストに失敗しました: {e}")
            
    except ValueError as e:
        # 入力検証エラー
        print(f"Input validation error: {e}")
        raise ValueError(f"入力データエラー: {e}")
        
    except RuntimeError as e:
        # 実行時エラー（すでにメッセージ付き）
        raise e
        
    except Exception as e:
        # その他の予期しないエラー
        print(f"Unexpected error in excuteGAS: {e}")
        raise RuntimeError(f"予期しないエラーが発生しました: {e}")