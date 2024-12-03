import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import ProtectedRoute from '@/components/ProtectedRoute';
import { auth } from '../firebase.js';
import { useRouter } from 'next/router';

interface Resume {
  questionnaire_id: number;
  name: string;
  date_created: string;
}

const Dashboard = () => {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);

  // Fetch resumes on component mount
  useEffect(() => {
    const fetchResumes = async () => {
      try {
        const user = auth.currentUser;
        if (user) {
          const idToken = await user.getIdToken();
          const apiUrl = `${process.env.NEXT_PUBLIC_API_URL}/resumes/`;
          const response = await axios.get(apiUrl, {
            headers: {
              Authorization: `Bearer ${idToken}`,
            },
          });
          setResumes(response.data.resumes);
        } else {
          setError('User not authenticated');
        }
      } catch (err) {
        console.error(err);
        setError('An error occurred while fetching resumes.');
      } finally {
        setLoading(false);
      }
    };

    fetchResumes();
  }, []);

  // Function to open PDF
  const openPDF = async (questionnaire_id: number) => {
    try {
      const user = auth.currentUser;
      if (user) {
        const idToken = await user.getIdToken();
        const uid = user.uid;

        const apiUrl = `${process.env.NEXT_PUBLIC_API_URL}/pdfs/${uid}/${questionnaire_id}`;
        const response = await axios.get(apiUrl, {
          headers: {
            Authorization: `Bearer ${idToken}`,
          },
          responseType: 'blob', // Expecting a PDF file
        });

        // Create a blob URL and open in new tab
        const pdfBlob = new Blob([response.data], { type: 'application/pdf' });
        const pdfUrl = URL.createObjectURL(pdfBlob);
        window.open(pdfUrl, '_blank');
      } else {
        setError('User not authenticated');
      }
    } catch (err) {
      console.error(err);
      setError('An error occurred while fetching the PDF.');
    }
  };

  const router = useRouter();

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <Navbar />

      {/* Dashboard Content */}
      <div className="container mx-auto py-10 px-4">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Your Resumes</h1>
          <button
            className="text-xl text-white bg-amber-500 px-4 py-2 rounded-full hover:bg-amber-600 transition"
            onClick={() => router.push('/resume')}
          >
            +
          </button>
        </div>

        {/* Error Message */}
        {error && <p className="text-red-500 mb-4">{error}</p>}

        {/* Loading Indicator */}
        {loading ? (
          <p>Loading...</p>
        ) : (
          <>
            {resumes.length === 0 ? (
              <p>No resumes found.</p>
            ) : (
              <div
                className="
                  grid
                  grid-cols-1
                  sm:grid-cols-2
                  md:grid-cols-3
                  lg:grid-cols-4
                  xl:grid-cols-5
                  2xl:grid-cols-6
                  gap-6
                  justify-items-center
                "
              >
                {resumes.map((resume) => (
                  <div
                    key={resume.questionnaire_id}
                    className="
                      relative
                      group
                      bg-white
                      rounded-lg
                      shadow-md
                      overflow-hidden
                      hover:shadow-lg
                      transition
                      cursor-pointer
                      max-w-xs
                      w-full
                    "
                    onClick={() => openPDF(resume.questionnaire_id)}
                  >
                    {/* Optional: Add a placeholder image or icon */}
                    <div className="h-40 bg-gray-200 flex items-center justify-center">
                      <svg
                        className="w-16 h-16 text-gray-400 group-hover:text-amber-500 transition"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path d="M4 3a2 2 0 00-2 2v2h16V5a2 2 0 00-2-2H4z" />
                        <path
                          fillRule="evenodd"
                          d="M18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM8 11h4v2H8v-2z"
                          clipRule="evenodd"
                        />
                      </svg>
                    </div>
                    <div className="p-4">
                      <h3 className="text-lg font-semibold text-gray-900 mb-2 text-center">
                        {resume.name || `Resume ${resume.questionnaire_id}`}
                      </h3>
                      <p className="text-gray-600 text-sm text-center">
                        Created on:{' '}
                        {new Date(resume.date_created).toLocaleDateString()}
                      </p>
                    </div>
                    {/* Optional: Overlay on hover */}
                    <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-10 transition"></div>
                  </div>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default ProtectedRoute(Dashboard);