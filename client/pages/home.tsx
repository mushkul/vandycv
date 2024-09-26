// pages/index.tsx
import Link from 'next/link';

const Home = () => {
    return (
        <div className="flex justify-center items-center min-h-screen bg-gradient-to-r from-yellow-50 to-yellow-100">
            <div className="text-center p-10">
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
                <div className="mt-10">
                    <img
                        src="/resume-preview.png" // Placeholder for the resume images you have in the design
                        alt="Resume Previews"
                        className="mx-auto w-96"
                    />
                </div>
                <div className="mt-8">
                    <Link href="/login">
                        <button className="bg-transparent border-none text-gray-600 hover:text-gray-900">
                            Log in
                        </button>
                    </Link>
                    <span className="mx-2">or</span>
                    <Link href="/signup">
                        <button className="bg-yellow-500 text-white font-bold py-2 px-4 rounded-md hover:bg-yellow-600 transition duration-300">
                            Sign up
                        </button>
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default Home;
