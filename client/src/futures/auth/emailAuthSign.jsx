import { auth } from "@/futures/auth/initFirebaseAuth";
import { createUserWithEmailAndPassword } from "firebase/auth";

export function emailAuthSign(email, password) {
    createUserWithEmailAndPassword(auth, email, password)
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