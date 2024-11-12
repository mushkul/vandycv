

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import ProtectedRoute from '@/components/ProtectedRoute';
import { auth } from '../firebase.js';  // Ensure you have the correct path
import { useRouter } from 'next/router'
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
              'Authorization': `Bearer ${idToken}`,
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
        // const decoded_token = auth.verify_id_token(idToken)
        // const uid = decoded_token['uid']
        const uid = user.uid;

        const apiUrl = `${process.env.NEXT_PUBLIC_API_URL}/pdfs/${uid}/${questionnaire_id}`;
        const response = await axios.get(apiUrl, {
          headers: {
            'Authorization': `Bearer ${idToken}`,
          },
          responseType: 'blob',  // Expecting a PDF file
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
    <div className="min-h-screen bg-gradient-to-r from-yellow-50 to-yellow-100">
      {/* Navbar */}
      <Navbar />

      {/* Dashboard Content */}
      <div className="container mx-auto py-10 px-4">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Recent Resumes</h1>
          <button
            className="text-xl text-gray-700 bg-yellow-300 px-4 py-2 rounded hover:bg-yellow-400 transition"
            onClick={() => router.push('/resume')}
          >
            +
          </button>
        </div>

        {/* Search Bar and Order By */}
        {/* Implement search and ordering functionality as needed */}

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
              <div className="grid grid-cols-1 gap-4">
                {resumes.map((resume) => (
                  <div
                    key={resume.questionnaire_id}
                    className="border border-gray-300 p-4 bg-white rounded-md shadow-md hover:shadow-lg transition cursor-pointer"
                    onClick={() => openPDF(resume.questionnaire_id)}
                  >
                    <h3 className="text-lg font-semibold text-gray-900">
                      Resume {resume.questionnaire_id}
                    </h3>
                    <p className="text-gray-600">Created at: {resume.date_created}</p>
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