// pages/index.js

import { useState } from 'react';

export default function Home() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    objective: '',
    education: '',
    experience: '',
    skills: '',
  });

  const [resume, setResume] = useState('');
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await fetch('http://localhost:5000/generate-resume', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      if (data.resume) {
        setResume(data.resume);
      } else {
        setError(data.error || 'An error occurred.');
      }
    } catch (err) {
      setError('Failed to connect to the server.');
    }
  };

  return (
    <div>
      <h1>Resume Generator</h1>
      <form onSubmit={handleSubmit}>
        {/* Input fields for name, email, phone, etc. */}
        <input type="text" name="name" placeholder="Name" onChange={handleChange} required />
        {/* Add other input fields similarly */}
        <button type="submit">Generate Resume</button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}
      {resume && (
        <div>
          <h2>Your Generated Resume:</h2>
          <pre>{resume}</pre>
        </div>
      )}
    </div>
  );
}
