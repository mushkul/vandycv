// pages/dashboard.tsx
import React from 'react';
import Navbar from '../components/Navbar';  // Importing the Navbar component
import ProtectedRoute from '@/components/ProtectedRoute';

const Dashboard = () => {
  return (
    <div className="min-h-screen bg-gradient-to-r from-yellow-50 to-yellow-100">
      {/* Navbar */}
      <Navbar />  {/* Including the Navbar here */}

      {/* Dashboard Content */}
      <div className="container mx-auto py-10 px-4">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Recent Resumes</h1>
          <button className="text-xl text-gray-700 bg-yellow-300 px-4 py-2 rounded hover:bg-yellow-400 transition">
            +
          </button>
        </div>

        {/* Search Bar and Order By */}
        <div className="flex justify-between items-center mb-6">
          <input
            type="text"
            placeholder="Search Resumes..."
            className="w-full max-w-lg px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500"
          />
          <select className="ml-4 px-4 py-2 border rounded-lg bg-white text-gray-700 focus:outline-none">
            <option>Order By</option>
            <option>Newest First</option>
            <option>Oldest First</option>
          </select>
        </div>

        {/* Resume Cards Placeholder */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Placeholder for individual resume cards */}
          {Array.from({ length: 9 }).map((_, index) => (
            <div
              key={index}
              className="border border-gray-300 p-4 bg-white rounded-md shadow-md hover:shadow-lg transition"
            >
              <div className="h-40 bg-gray-200 rounded-md mb-4"></div>
              <h3 className="text-lg font-semibold text-gray-900">Document Title</h3>
              <p className="text-gray-600">Date Created</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProtectedRoute(Dashboard);
