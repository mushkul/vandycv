import Link from 'next/link';
import { useRouter } from 'next/router';
import { signOut, onAuthStateChanged } from 'firebase/auth';
import { useEffect, useState } from 'react';
import { auth } from '../firebase'; // Import Firebase auth instance

const Navbar = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false); // State to check if user is logged in
    const router = useRouter();

    // Check if user is logged in when component mounts
    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, (user) => {
            if (user) {
                setIsLoggedIn(true);  // User is logged in
            } else {
                setIsLoggedIn(false); // User is not logged in
            }
        });

        return () => unsubscribe(); // Clean up the observer on unmount
    }, []);

    const handleLogout = async () => {
        try {
            await signOut(auth);
            alert('You have successfully logged out!');
            router.push('/home'); // Redirect to the home page after logout
        } catch (error) {
            console.error('Error logging out: ', error);
        }
    };

    const handleHomeClick = (e: { preventDefault: () => void; }) => {
        e.preventDefault();
        if (isLoggedIn) {
            router.push('/dashboard'); // Redirect to dashboard if logged in
        } else {
            router.push('/home'); // Redirect to home page if not logged in
        }
    };

    return (
        <nav className="bg-gray-900 shadow-md">
            <div className="max-w-6xl mx-auto px-4">
                <div className="flex justify-between items-center h-16">
                    <div className="flex items-center space-x-8">
                        <Link href="/" className="flex-shrink-0">
                            <span className="text-xl font-bold" style={{ color: '#CFAE70' }}>VandyCV</span>
                        </Link>
                        <div className="hidden md:flex items-center space-x-4">
                            {/* Home link with conditional routing */}
                            <a
                                href="#"
                                onClick={handleHomeClick}
                                className={`text-white hover:text-gray-300 px-3 py-2 rounded-md text-sm font-medium ${router.pathname === '/' ? 'bg-gray-800' : ''
                                    }`}
                            >
                                Home
                            </a>
                            <Link
                                href="/resume"
                                className={`text-white hover:text-gray-300 px-3 py-2 rounded-md text-sm font-medium ${router.pathname === '/resume' ? 'bg-gray-800' : ''
                                    }`}
                            >
                                Resume
                            </Link>
                        </div>
                    </div>
                    <div>
                        {/* Conditional rendering for the Logout button if the user is logged in */}
                        {isLoggedIn ? (
                            <button onClick={handleLogout} className="text-white hover:text-gray-300 px-3 py-2 rounded-md text-sm font-medium">
                                Logout
                            </button>
                        ) : (
                            <Link href="/login" className="text-white hover:text-gray-300 px-3 py-2 rounded-md text-sm font-medium">
                                Login
                            </Link>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;