import { auth } from "@/futures/auth/initFirebaseAuth";
import { signInWithEmailAndPassword } from "firebase/auth";

export function emailAuthLogin(email, password) {
    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            const user = userCredential.user;
            return {
                status: 200,
                error: false,
                user: user
            }
        })
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
            console.log(errorCode, errorMessage);
            return {
                status: 500,
                error: true,
                errorCode: errorCode,
                errorMessage: errorMessage
            }
        });
}