import { useState } from 'react';
import { getAuth, signInWithEmailAndPassword } from 'firebase/auth';  // Import from firebase/auth
import { auth } from './firebase';  // Assuming auth is already initialized in firebase.js

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const auth = getAuth();  // Get the Auth instance
      const userCredential = await signInWithEmailAndPassword(auth, email, password);  // Pass auth, email, and password
      const idToken = await userCredential.user.getIdToken();
      
      // Send the token to the backend
      const response = await fetch('http://localhost:3000/api/profile', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${idToken}`,  // Send token in Authorization header
        },
      });

      const data = await response.json();
      if (response.ok) {
        console.log('Authenticated User:', data);
      } else {
        console.error('Error:', data.error);
      }
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
      <button type="submit">Login</button>
    </form>
  );
}

export default Login;
