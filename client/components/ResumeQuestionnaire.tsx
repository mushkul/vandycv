// ResumeQuestionnaire.tsx

import axios from 'axios';
import React, { useState } from 'react';
import { auth } from '../firebase.js';

// Define interfaces for TypeScript
interface JobExperience {
    name: string;
    title: string;
    location: string;
    description: string;
}

interface FormData {
    firstName: string;
    lastName: string;
    middleInitial?: string;
    address?: string;
    email: string;
    contactNumber: string;
    linkedinLink?: string;
    githubLink?: string;
    college: string;
    majorConcentration: string;
    secondMajor?: string;
    gpa?: string;
    locationOfCollege: string;
    startYear: string;
    endYear: string;
    relevantCoursework?: string;
    jobExperiences: JobExperience[];
}

// JobExperienceForm component
const JobExperienceForm: React.FC<{
    experience: JobExperience;
    index: number;
    onChange: (index: number, field: string, value: string) => void;
}> = ({ experience, index, onChange }) => (
    <section key={index} className="relative pl-12 mb-12">
        {/* Vertical line */}
        <div className="absolute left-5 top-0 w-0.5 h-full bg-gray-300"></div>
        {/* Circle indicator */}
        <div className="absolute left-4 top-0 w-3 h-3 bg-white border-2 border-amber-500 rounded-full"></div>
        <h2 className="text-xl font-semibold mb-4">Job Experience #{index + 1}</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Job Name */}
            <div>
                <label className="block mb-1">Job Name: *</label>
                <input
                    type="text"
                    name="name"
                    value={experience.name}
                    onChange={(e) => onChange(index, 'name', e.target.value)}
                    required
                    className="w-full p-2 border rounded bg-amber-50"
                />
            </div>
            {/* Title */}
            <div>
                <label className="block mb-1">Title: *</label>
                <input
                    type="text"
                    name="title"
                    value={experience.title}
                    onChange={(e) => onChange(index, 'title', e.target.value)}
                    required
                    className="w-full p-2 border rounded bg-amber-50"
                />
            </div>
            {/* Location */}
            <div>
                <label className="block mb-1">Location: *</label>
                <input
                    type="text"
                    name="location"
                    value={experience.location}
                    onChange={(e) => onChange(index, 'location', e.target.value)}
                    required
                    className="w-full p-2 border rounded bg-amber-50"
                />
            </div>
            {/* Description */}
            <div className="col-span-2">
                <label className="block mb-1">Short Description of what you did: *</label>
                <textarea
                    name="description"
                    value={experience.description}
                    onChange={(e) => onChange(index, 'description', e.target.value)}
                    required
                    className="w-full p-2 border rounded bg-amber-50"
                    rows={4}
                ></textarea>
            </div>
        </div>
    </section>
);

const ResumeQuestionnaire: React.FC = () => {
    // Initial state for form data
    const [formData, setFormData] = useState<FormData>({
        firstName: '',
        lastName: '',
        middleInitial: '',
        address: '',
        email: '',
        contactNumber: '',
        linkedinLink: '',
        githubLink: '',
        college: '',
        majorConcentration: '',
        secondMajor: '',
        gpa: '',
        locationOfCollege: '',
        startYear: '',
        endYear: '',
        relevantCoursework: '',
        jobExperiences: [{ name: '', title: '', location: '', description: '' }],
    });

    // State variables for loading and error handling
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>('');

    const handleChange = (
        e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
    ) => {
        const { name, value } = e.target;
        setFormData((prevState) => ({
            ...prevState,
            [name]: value,
        }));
    };

    const handleJobExperienceChange = (
        index: number,
        field: string,
        value: string
    ) => {
        setFormData((prevState) => {
            const updatedExperiences = [...prevState.jobExperiences];
            updatedExperiences[index] = {
                ...updatedExperiences[index],
                [field]: value,
            };
            return { ...prevState, jobExperiences: updatedExperiences };
        });
    };

    const addJobExperience = () => {
        if (formData.jobExperiences.length < 4) {
            setFormData((prevState) => ({
                ...prevState,
                jobExperiences: [
                    ...prevState.jobExperiences,
                    { name: '', title: '', location: '', description: '' },
                ],
            }));
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        // Basic validation
        if (
            !formData.firstName ||
            !formData.lastName ||
            !formData.email ||
            !formData.contactNumber
        ) {
            setError('Please fill in all required fields.');
            setLoading(false);
            return;
        }

        try {
            const apiUrl = `${process.env.NEXT_PUBLIC_API_URL}/generateresume/`;

            const user = auth.currentUser;
            if (user) {
                // Get the ID token
                const idToken = await user.getIdToken();

                // Make the request with the ID token in the Authorization header
                const response = await axios.post(apiUrl, formData, {
                    headers: {
                        Authorization: `Bearer ${idToken}`,
                    },
                    responseType: 'blob',
                });

                const pdfBlob = new Blob([response.data], { type: 'application/pdf' });
                const pdfUrl = URL.createObjectURL(pdfBlob);

                // Open the PDF in a new tab
                window.open(pdfUrl, '_blank');
            } else {
                setError('User not authenticated');
                setLoading(false);
                return;
            }
        } catch (err) {
            console.error(err);
            setError('An error occurred while generating the resume.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto p-6 bg-white">
            <h1 className="text-3xl font-bold mb-6 text-center py-2">
                Resume Survey
            </h1>
            <p className="text-right mb-4 text-sm">
                Questions marked with * are required
            </p>

            <form onSubmit={handleSubmit} className="space-y-12 relative">
            

                {/* Vertical line */}
                <div className="absolute left-5 top-0 w-0.5 h-full bg-gray-300"></div>

                {/* Personal Information Section */}
                <section className="relative pl-12">
                    {/* Circle indicator */}
                    <div className="absolute left-4 top-0 w-3 h-3 bg-white border-2 border-amber-500 rounded-full"></div>
                    <h2 className="text-xl font-semibold mb-4">Personal Information</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {/* First Name */}
                        <div>
                            <label className="block mb-1">First name: *</label>
                            <input
                                type="text"
                                name="firstName"
                                value={formData.firstName}
                                onChange={handleChange}
                                required
                                className="w-full p-2 border rounded bg-amber-50"
                                placeholder="First Name"
                            />
                        </div>
                        {/* Last Name */}
                        <div>
                            <label className="block mb-1">Last name: *</label>
                            <input
                                type="text"
                                name="lastName"
                                value={formData.lastName}
                                onChange={handleChange}
                                required
                                className="w-full p-2 border rounded bg-amber-50"
                                placeholder="Last Name"
                            />
                        </div>
                        {/* Middle Initial */}
                        <div>
                            <label className="block mb-1">Middle Initial:</label>
                            <input
                                type="text"
                                name="middleInitial"
                                value={formData.middleInitial}
                                onChange={handleChange}
                                maxLength={1}
                                className="w-full p-2 border rounded bg-amber-50"
                                placeholder="M"
                            />
                        </div>
                        {/* Address */}
                        <div>
                            <label className="block mb-1">Address:</label>
                            <input
                                type="text"
                                name="address"
                                value={formData.address}
                                onChange={handleChange}
                                className="w-full p-2 border rounded bg-amber-50"
                                placeholder="123 Main St, City, State"
                            />
                        </div>
                        {/* Email */}
                        <div>
                            <label className="block mb-1">Email: *</label>
                            <input
                                type="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                required
                                className="w-full p-2 border rounded bg-amber-50"
                                placeholder="you@example.com"
                            />
                        </div>
                        {/* Contact Number */}
                        <div>
                            <label className="block mb-1">Contact Number: *</label>
                            <input
                                type="tel"
                                name="contactNumber"
                                value={formData.contactNumber}
                                onChange={handleChange}
                                required
                                className="w-full p-2 border rounded bg-amber-50"
                                placeholder="1234567890"
                            />
                        </div>
                        {/* LinkedIn Link */}
                        <div>
                            <label className="block mb-1">LinkedIn Link:</label>
                            <input
                                type="url"
                                name="linkedinLink"
                                value={formData.linkedinLink}
                                onChange={handleChange}
                                className="w-full p-2 border rounded bg-amber-50"
                                placeholder="https://www.linkedin.com/in/yourprofile"
                            />
                        </div>
                        {/* GitHub Link */}
                        <div>
                            <label className="block mb-1">GitHub Link:</label>
                            <input
                                type="url"
                                name="githubLink"
                                value={formData.githubLink}
                                onChange={handleChange}
                                className="w-full p-2 border rounded bg-amber-50"
                                placeholder="https://github.com/yourusername"
                            />
                        </div>
                    </div>
                </section>

                {/* Education Section */}
                <section className="relative pl-12">
                    {/* Circle indicator */}
                    <div className="absolute left-4 top-0 w-3 h-3 bg-white border-2 border-amber-500 rounded-full"></div>
                    <h2 className="text-xl font-semibold mb-4">Education</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {/* College */}
                        <div>
                            <label className="block mb-1">College: *</label>
                            <input
                                type="text"
                                name="college"
                                value={formData.college}
                                onChange={handleChange}
                                required
                                className="w-full p-2 border rounded bg-amber-50"
                                placeholder="University of Example"
                            />
                        </div>
                        {/* Major/Concentration */}
                        <div>
                            <label className="block mb-1">Major/Concentration: *</label>
                            <input
                                type="text"
                                name="majorConcentration"
                                value={formData.majorConcentration}
                                onChange={handleChange}
                                required
                                className="w-full p-2 border rounded bg-amber-50"
                                placeholder="Computer Science"
                            />
                        </div>
                        {/* Second Major */}
                        <div>
                            <label className="block mb-1">Second Major:</label>
                            <input
                                type="text"
                                name="secondMajor"
                                value={formData.secondMajor}
                                onChange={handleChange}
                                className="w-full p-2 border rounded bg-amber-50"
                                placeholder="Mathematics"
                            />
                        </div>
                        {/* GPA */}
                        <div>
                            <label className="block mb-1">GPA:</label>
                            <input
                                type="text"
                                name="gpa"
                                value={formData.gpa}
                                onChange={handleChange}
                                className="w-full p-2 border rounded bg-amber-50"
                                placeholder="3.8"
                            />
                        </div>
                        {/* Location of College */}
                        <div>
                            <label className="block mb-1">Location of College: *</label>
                            <input
                                type="text"
                                name="locationOfCollege"
                                value={formData.locationOfCollege}
                                onChange={handleChange}
                                required
                                className="w-full p-2 border rounded bg-amber-50"
                                placeholder="City, State"
                            />
                        </div>
                        {/* Start and End Year */}
                        <div className="flex gap-4">
                            <div className="flex-1">
                                <label className="block mb-1">Start Year: *</label>
                                <input
                                    type="text"
                                    name="startYear"
                                    value={formData.startYear}
                                    onChange={handleChange}
                                    required
                                    className="w-full p-2 border rounded bg-amber-50"
                                    placeholder="2018"
                                />
                            </div>
                            <div className="flex-1">
                                <label className="block mb-1">End Year: *</label>
                                <input
                                    type="text"
                                    name="endYear"
                                    value={formData.endYear}
                                    onChange={handleChange}
                                    required
                                    className="w-full p-2 border rounded bg-amber-50"
                                    placeholder="2022"
                                />
                            </div>
                        </div>
                        {/* Relevant Coursework */}
                        <div className="col-span-2">
                            <label className="block mb-1">Relevant Coursework:</label>
                            <textarea
                                name="relevantCoursework"
                                value={formData.relevantCoursework}
                                onChange={handleChange}
                                className="w-full p-2 border rounded bg-amber-50"
                                rows={3}
                                placeholder="Algorithms, Data Structures, Operating Systems..."
                            ></textarea>
                        </div>
                    </div>
                </section>

                {/* Job Experience Section */}
                {formData.jobExperiences.map((experience, index) => (
                    <JobExperienceForm
                        key={index}
                        experience={experience}
                        index={index}
                        onChange={handleJobExperienceChange}
                    />
                ))}

                {formData.jobExperiences.length < 4 && (
                    <div className="text-center">
                        <button
                            type="button"
                            onClick={addJobExperience}
                            className="bg-amber-400 text-white px-4 py-2 rounded hover:bg-amber-500 transition-colors"
                        >
                            Add New Experience
                        </button>
                    </div>
                )}

                {/* Submit Button */}
                <div className="text-center">
                    <button
                        type="submit"
                        className="bg-amber-500 text-white px-6 py-2 rounded hover:bg-amber-600 transition-colors"
                    >
                        Submit
                    </button>
                </div>
            </form>

            {/* Display loading and error messages */}
            {loading && <p className="text-center mt-6">Generating your resume...</p>}
            {error && <p className="text-center text-red-500 mt-6">{error}</p>}
        </div>
    );
};

export default ResumeQuestionnaire;