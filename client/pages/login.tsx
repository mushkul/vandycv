// pages/login.tsx
import { useState, FormEvent } from 'react';
import axios from 'axios'; // if using axios

// TypeScript interface for form state
interface LoginFormState {
  email: string;
  password: string;
}

const Login = () => {
  // Form state management
  const [formData, setFormData] = useState<LoginFormState>({ email: '', password: '' });
  const [error, setError] = useState<string>('');

  // Form input change handler
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // Handle form submission
  const handleLogin = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/login', formData);
      if (response.data.success) {
        // Handle successful login (e.g., redirect to a dashboard)
        alert('Login Successful!');
      } else {
        setError(response.data.message);
      }
    } catch (err) {
      setError('Login failed. Please check your credentials.');
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gradient-to-r from-yellow-50 to-yellow-100">
      <div className="bg-white p-10 rounded shadow-lg">
        <h1 className="text-3xl font-bold mb-4">Login to your account</h1>
        {error && <p className="text-red-500 mb-4">{error}</p>}
        <form onSubmit={handleLogin}>
          <div className="mb-4">
            <label className="block text-sm font-bold mb-2">Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <div className="mb-4">
            <div className="flex justify-between items-center mb-2">
              <label className="block text-sm font-bold">Password</label>
              <a href="/forgot-password" className="text-sm text-blue-500 hover:text-blue-700">
                Forgot?
              </a>
            </div>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-yellow-500 text-white font-bold py-2 px-4 rounded"
          >
            Login now
          </button>
          <div className="flex justify-center items-center mb-2">
            <label className="block text-sm mr-5">
              Don't have an account? </label>
            <a href="/signup" className="text-sm text-blue-500 hover:text-blue-700">Sign up</a>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
