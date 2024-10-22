// pages/signup.tsx
import { useState, FormEvent } from 'react';
import { createUserWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../firebase';
import { useRouter } from 'next/router';  // Import the useRouter hook
import Link from 'next/link';

interface SignupFormState {
    email: string;
    password: string;
}

const Signup = () => {
    const [formData, setFormData] = useState<SignupFormState>({ email: '', password: '' });
    const [error, setError] = useState<string>('');
    const router = useRouter(); // Initialize the useRouter hook for navigation

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSignup = async (e: FormEvent) => {
        e.preventDefault();
        setError(''); // Clear previous errors
        try {
          const userCredential = await createUserWithEmailAndPassword(auth, formData.email, formData.password);
          console.log(userCredential.user); // You can handle this user object as needed
          alert('Signup Successful!');
          router.push('/dashboard')
        } catch (err: any) {
            // Handle Firebase errors
            switch (err.code) {
                case 'auth/email-already-in-use':
                    setError('The email address is already in use. Please use a different email.');
                    break;
                case 'auth/invalid-email':
                    setError('The email address is invalid. Please enter a valid email.');
                    break;
                case 'auth/weak-password':
                    setError('The password is too weak. Please enter a stronger password (at least 6 characters).');
                    break;
                case 'auth/operation-not-allowed':
                    setError('Sign up with email and password is not enabled.');
                    break;
                default:
                    setError('Failed to create an account. Please try again.');
            }
        }
      };

    return (
        <div className="flex justify-center items-center h-screen bg-gradient-to-r from-yellow-50 to-yellow-100">
            <div className="bg-white p-10 rounded shadow-lg w-96">
                <h1 className="text-3xl font-bold mb-6 text-center">VandyCV</h1>
                <h2 className="text-2xl font-semibold mb-6 text-center">Create an account</h2>
                {error && <p className="text-red-500 mb-4">{error}</p>}
                <form onSubmit={handleSignup}>
                    <div className="mb-4">
                        <label className="block text-sm font-medium mb-2">Email</label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            required
                            className="w-full px-3 py-2 border rounded-md"
                            placeholder="balamia@gmail.com"
                        />
                    </div>
                    <div className="mb-6">
                        <div className="flex justify-between items-center mb-2">
                            <label className="block text-sm font-medium">Password</label>
                            <Link href="/forgot-password" className="text-sm text-blue-500 hover:text-blue-700">
                                Forgot?
                            </Link>
                        </div>
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            required
                            className="w-full px-3 py-2 border rounded-md"
                            placeholder="Enter your password"
                        />
                    </div>
                    <button
                        type="submit"
                        className="w-full bg-yellow-500 text-white font-bold py-2 px-4 rounded-md hover:bg-yellow-600 transition duration-300"
                    >
                        Create account
                    </button>
                </form>
                <div className="mt-6 text-center">
                    <p className="text-sm text-gray-600">
                        Already Have An Account?{' '}
                        <Link href="/login" className="text-blue-500 hover:text-blue-700">
                            Log In
                        </Link>
                    </p>
                </div>
                <div className="mt-6 flex items-center justify-center">
                    <span className="text-gray-500 text-sm">Or</span>
                </div>
                <div className="mt-4 grid grid-cols-2 gap-4">
                    <button className="hover:bg-gray-50" type="submit">
                        <img src="/google-icon.png" alt="Google" />
                    </button>
                    <button className="hover:bg-gray-50">
                        <img src="/facebook-icon.png" alt="Facebook" />
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Signup;