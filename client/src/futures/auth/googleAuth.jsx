import { auth, signInWithPopup, GoogleAuthProvider } from "firebase/auth";

const provider = new GoogleAuthProvider();

export function googleAuthLogin() {
    signInWithPopup(auth, provider)
        .then((result) => {
            const user = result.user;
            return {
                status: 200,
                error: false,
                user: user
            }
        }).catch((error) =>{
            const errorCode = error.code;
            const errorMessage = error.message;
            const email = error.customData.email;
            const credential = GoogleAuthProvider.credentialFromError(error);
            return {
                status: 500,
                error: true,
                errorCode: errorCode,
                errorMessage: errorMessage,
                email: email
            }
        });
}
