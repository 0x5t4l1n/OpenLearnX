// lib/firebase.ts
import { initializeApp, getApps, getApp } from "firebase/app"
import { getAuth } from "firebase/auth"
// import { getAnalytics } from "firebase/analytics"; // Analytics can be initialized if needed

const firebaseConfig = {
  apiKey: "***************************************",
  authDomain: "*************************************",
  projectId: "************",
  storageBucket: "************************************",
  messagingSenderId: "************",
  appId: "**********************************************",
  measurementId: "************",
}

// Initialize Firebase
const app = !getApps().length ? initializeApp(firebaseConfig) : getApp()
const auth = getAuth(app)
// const analytics = getAnalytics(app); // Uncomment if you need analytics

export { app, auth }
