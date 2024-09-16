const express = require('express');
const admin = require('firebase-admin');
const cors = require('cors');
const dotenv = require('dotenv');
const app = express();

dotenv.config();  // Load environment variables

// Middleware
app.use(cors());
app.use(express.json());

// Firebase Admin SDK setup
const serviceAccount = require('./firebaseServiceAccount.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

// Example route to verify Firebase tokens
app.get('/api/profile', async (req, res) => {
  const token = req.headers.authorization?.split(' ')[1];  // Extract token
  if (!token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  try {
    const decodedToken = await admin.auth().verifyIdToken(token);
    res.json({ message: 'Authenticated', uid: decodedToken.uid });
  } catch (error) {
    res.status(401).json({ error: 'Invalid Token' });
  }
});

// Start the server
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
