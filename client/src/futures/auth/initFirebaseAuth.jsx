import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
    apiKey: "your-api-key",
    authDomain: "pos-system-for-soshosai.firebaseapp.com",
    projectId: "pos-system-for-soshosai",
    storageBucket: "pos-system-for-soshosai.firebasestorage.app",
    messagingSenderId: "your-messaging-sender-id",
    appId: "your-app-id"
};

const app = initializeApp(firebaseConfig);

const auth = getAuth(app);

export { auth };