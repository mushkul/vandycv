// src/firebase.js
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "AIzaSyBTj78qpJamN4FFv_iK1ddmf16UWaF-Guw",
  authDomain: "vandycv-743ae.firebaseapp.com",
  projectId: "vandycv-743ae",
  storageBucket: "vandycv-743ae.appspot.com",
  messagingSenderId: "820274774200",
  appId: "1:820274774200:web:de1738fcbc858fff84b44d",
  measurementId: "G-DXJXYZPBSP"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);