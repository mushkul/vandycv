// pages/index.tsx
import Link from 'next/link';

const Home = () => {
    return (
        <div className="min-h-screen bg-gradient-to-r from-yellow-50 to-yellow-100">
            {/* Header Section */}
            <header className="flex justify-between items-center p-4 shadow-lg bg-white">
                <div className="flex items-center">
                    {/* Logo / Site Title */}
                    <Link href="/" className="text-2xl font-bold text-yellow-600">
                        Vandy<span className="text-black">CV</span>
                    </Link>

                    {/* Navigation Menu */}
                    <nav className="ml-10 space-x-8">
                        <Link href="/" className="text-gray-700 hover:text-black">
                            Home
                        </Link>
                        <Link href="/resume" className="text-gray-700 hover:text-black">
                            Resume
                        </Link>
                        <Link href="/cover-letter" className="text-gray-700 hover:text-black">
                            Cover Letter
                        </Link>
                    </nav>
                </div>

                {/* Auth Buttons */}
                <div className="space-x-4">
                    <Link href="/login">
                        <button className="border border-gray-400 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-50 transition duration-300">
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
            <main className="flex flex-col justify-center items-center text-center pt-16 p-10">
                <h1 className="text-5xl font-bold mb-4">Get dream jobs with our</h1>
                <h2 className="text-5xl font-extrabold mb-6 text-gray-800">
                    <span className="text-yellow-500">AI Powered</span> resume builder
                </h2>
                <p className="text-xl mb-10">
                    Build a professional and personal resume tailored to your major and career
                </p>
                <div className="flex justify-center space-x-4">
                    <Link href="/resume">
                        <button className="bg-yellow-500 text-white font-bold py-3 px-8 rounded-md hover:bg-yellow-600 transition duration-300">
                            Create Resume
                        </button>
                    </Link>
                    <Link href="/cover-letter">
                        <button className="border border-yellow-500 text-yellow-500 font-bold py-3 px-8 rounded-md hover:bg-yellow-600 hover:text-white transition duration-300">
                            Create Cover Letter
                        </button>
                    </Link>
                </div>

                {/* Sample Resumes */}
                <div className="relative w-full h-96 mt-16">
                    <img
                        src="/Sample-Resume-Left.png" // Left resume image
                        alt="Resume Left"
                        className="absolute left-[5%] top-10 w-100 h-auto z-10"
                    />
                    <img
                        src="/Sample-Resume-Right.png" // Right resume image
                        alt="Resume Right"
                        className="absolute right-[5%] top-10 w-100 h-auto z-10"
                    />
                    <img
                        src="/Sample-Resume-Middle.png" // Middle resume image
                        alt="Resume Middle"
                        className="absolute left-1/2 transform -translate-x-1/2 top-0 w-100 h-auto z-20"
                    />
                </div>
            </main>
        </div>
    );
};

export default Home;
