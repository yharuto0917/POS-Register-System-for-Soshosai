// このテストコードは、Firebase Local Emulator Suiteが実行されている環境で動作させることを想定しています。
// 実行前に `firebase emulators:start` を実行してください。

// 必要なFirebaseモジュールをインポートします
// package.jsonに "firebase" が追加されている必要があります。
const { initializeApp } = require("firebase/app");
const { getFunctions, httpsCallable, connectFunctionsEmulator } = require("firebase/functions");

// Firebaseプロジェクトの設定情報を入力します。
// エミュレータを使用するため、実際のものである必要はありませんが、
// projectIdはご自身のFirebaseプロジェクトのIDに置き換える必要があります。
// プロジェクトIDは `firebase projects:list` コマンドで確認できます。
const firebaseConfig = {
  apiKey: "your-api-key",
  authDomain: "your-project-id.firebaseapp.com",
  projectId: "pos-system-for-soshosai", // ログに合わせて変更
  storageBucket: "your-project-id.appspot.com",
  messagingSenderId: "your-messaging-sender-id",
  appId: "your-app-id"
};

// Firebaseアプリを初期化します
const app = initializeApp(firebaseConfig);
const functions = getFunctions(app);

// Functionsエミュレータに接続します
// functionsエミュレータがデフォルトのポート(5001)で起動していることを確認してください。
connectFunctionsEmulator(functions, "localhost", 5001);

/**
 * `on_call_backend`関数をテストするための非同期関数
 */
async function testExcuteGAS() {
  console.log("`excuteGAS`のテストを開始します...");

  try {
    // `on_call_backend`関数への参照を取得します。
    // 関数名はmain.pyでデプロイされている名前に合わせます(`on_call_backend`)。
    const onCallBackend = httpsCallable(functions, 'on_call_backend');
    
    // `geminiAnalyze`を呼び出すためのデータを作成します
    const jsonInf = testProcessOrder();
    const data = {
      function_name: "excuteGAS",
      contents: jsonInf
    };

    // 関数を呼び出します
    console.log("Cloud Functionを呼び出します。データ:", JSON.stringify(data, null, 2));
    onCallBackend(data).then((result) => {
      console.log("Cloud Functionからのレスポンス:", result.data);
    }).catch((error) => {
      console.error("functions/main.pyからのエラー:", error.code, error.message);
    });
  } catch (error) {
    console.error("テスト中にエラーが発生しました:", error.code, error.message);
  }
}

function testProcessOrder() {
  // テスト用のサンプル注文データ
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
}

// テストを実行します
testExcuteGAS();
