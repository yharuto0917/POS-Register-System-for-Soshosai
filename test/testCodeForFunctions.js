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
async function testGeminiAnalyze() {
  console.log("`geminiAnalyze`のテストを開始します...");

  try {
    // `on_call_backend`関数への参照を取得します。
    // 関数名はmain.pyでデプロイされている名前に合わせます(`on_call_backend`)。
    const onCallBackend = httpsCallable(functions, 'on_call_backend');
    
    // `geminiAnalyze`を呼び出すためのデータを作成します
    const data = {
      function_name: "geminiAnalyze",
      contents: "これはGeminiの分析機能のテストメッセージです。"
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

// テストを実行します
testGeminiAnalyze();
