// pages/index.tsx
import Link from 'next/link';

const Home = () => {
    return (
        <div className="min-h-screen flex flex-col">
            {/* Header Section */}
            <header className="flex justify-between items-center p-4 shadow-lg bg-gray-900 shadow-md ">
                <div className="flex items-center ">
                    {/* Logo / Site Title */}
                    <Link href="/" className="text-2xl font-bold" style={{ color: '#CFAE70' }}>
                        VandyCV
                    </Link>

                    {/* Navigation Menu */}
                    <nav className="ml-10 space-x-8">
                        <Link href="/" className="text-white ">
                            Home
                        </Link>
                        <Link href="/resume" className="text-white ">
                            Resume
                        </Link>
                    </nav>
                </div>

                {/* Auth Buttons */}
                <div className="space-x-4">
                    <Link href="/login">
                        <button className="border border-gray-400 text-white py-2 px-4 rounded-md hover:bg-blue-950 transition duration-300">
                            Log in
                        </button>
                    </Link>
                    <Link href="/signup">
                        <button className="bg-yellow-500 text-white font-bold py-2 px-4 rounded-md hover:bg-yellow-600 transition duration-300">
                            Sign up
                        </button>
                    </Link>
                </div>
            </header>

            {/* Main Body*/}
            <main className="flex-grow flex flex-col justify-center items-center text-center">
                <h1 className="text-5xl font-bold mb-4">Get dream jobs with our</h1>
                <h2 className="text-5xl font-extrabold mb-6 text-gray-800">
                    <span className="text-yellow-500">AI Powered</span> resume builder
                </h2>
                <p className="text-xl mb-10">
                    Build a professional and personal resume tailored to your major and career
                </p>
                <div className="flex justify-center space-x-4">
                    <Link href="/login">
                        <button className="bg-yellow-500 text-white font-bold py-3 px-8 rounded-md hover:bg-yellow-600 transition duration-300">
                            Create Resume
                        </button>
                    </Link>
                </div>
            </main>
        </div>
    );
};

export default Home;
