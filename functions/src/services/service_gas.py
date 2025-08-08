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
    url = 'https://script.google.com/macros/s/AKfycbx98s3DUuJQRKnB0OOHe3GjGQadKSY7JzYAFsKBCh3Cj3w1ran0c2pzplDD9hvpCHbF/exec'
    
    try:
        response = requests.post(url, json=contents)
        # HTTPステータスコードが 2xx (成功) でない場合に例外を発生させます
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        # GASからの応答がJSON形式でない場合のエラーです
        print(f"Error: Failed to decode JSON from GAS. Response text: {response.text}")
        return {"error": "Invalid JSON response from GAS", "details": response.text}
    except requests.exceptions.RequestException as e:
        # ネットワークエラーやHTTPエラーの場合
        print(f"Error: Request to GAS failed: {e}")
        return {"error": "Failed to communicate with GAS", "details": str(e)}