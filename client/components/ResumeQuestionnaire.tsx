import React, { useState } from 'react';

const JobExperienceForm = ({ experience, index, onChange }) => (
    <section key={index}>
        <h2 className="text-xl font-semibold mb-4">Job Experience #{index + 1}</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
            <div className="col-span-2">
                <label className="block mb-1"> Short Description of what you did: *</label>
                <textarea
                    name="description"
                    value={experience.description}
                    onChange={(e) => onChange(index, 'description', e.target.value)}
                    required
                    className="w-full p-2 border rounded bg-amber-50"
                    rows="4"
                ></textarea>
            </div>
        </div>
    </section>
);


const ResumeQuestionnaire = () => {
    const [formData, setFormData] = useState({
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
        jobExperienceName: '',
        jobExperienceTitle: '',
        jobExperienceLocation: '',
        jobExperienceDescription: '',
        jobExperiences: [
            { name: '', title: '', location: '', description: '' }
        ]
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(formData);
        // Here you would typically send the data to your backend
    };

    const handleJobExperienceChange = (index, field, value) => {
        setFormData(prevState => {
            const updatedExperiences = [...prevState.jobExperiences];
            updatedExperiences[index] = { ...updatedExperiences[index], [field]: value };
            return { ...prevState, jobExperiences: updatedExperiences };
        });
    };

    const addJobExperience = () => {
        if (formData.jobExperiences.length < 4) {
            setFormData(prevState => ({
                ...prevState,
                jobExperiences: [...prevState.jobExperiences, { name: '', title: '', location: '', description: '' }]
            }));
        }
    };

    return (
        <div className="max-w-4xl mx-auto p-6 bg-amber-100 rounded-lg shadow-lg">
            <h1 className="text-3xl font-bold mb-6 text-center bg-amber-300 py-2 rounded">Resume Survey</h1>
            <p className="text-right mb-4 text-sm">Questions marked with * are required</p>

            <form onSubmit={handleSubmit} className="space-y-6">
                <section>
                    <h2 className="text-xl font-semibold mb-4">Personal Information</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label className="block mb-1">First name: *</label>
                            <input
                                type="text"
                                name="firstName"
                                value={formData.firstName}
                                onChange={handleChange}
                                required
                                className="w-full p-2 border rounded bg-amber-50"
                            />
                        </div>
                        <div>
                            <label className="block mb-1">Last name: *</label>
                            <input
                                type="text"
                                name="lastName"
                                value={formData.lastName}
                                onChange={handleChange}
                                required
                                className="w-full p-2 border rounded bg-amber-50"
                            />
                        </div>
                        <div>
                            <label className="block mb-1">Middle Initial:</label>
                            <input
                                type="text"
                                name="middleInitial"
                                value={formData.middleInitial}
                                onChange={handleChange}
                                maxLength="1"
                                className="w-full p-2 border rounded bg-amber-50"
                            />
                        </div>
                        <div>
                            <label className="block mb-1">Address:</label>
                            <input
                                type="text"
                                name="address"
                                value={formData.address}
                                onChange={handleChange}
                                className="w-full p-2 border rounded bg-amber-50"
                            />
                        </div>
                        <div>
                            <label className="block mb-1">Email: *</label>
                            <input
                                type="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                required
                                className="w-full p-2 border rounded bg-amber-50"
                            />
                        </div>
                        <div>
                            <label className="block mb-1">Contact Number: *</label>
                            <input
                                type="tel"
                                name="contactNumber"
                                value={formData.contactNumber}
                                onChange={handleChange}
                                required
                                className="w-full p-2 border rounded bg-amber-50"
                            />
                        </div>
                        <div>
                            <label className="block mb-1">LinkedIn Link:</label>
                            <input
                                type="url"
                                name="linkedinLink"
                                value={formData.linkedinLink}
                                onChange={handleChange}
                                className="w-full p-2 border rounded bg-amber-50"
                            />
                        </div>
                        <div>
                            <label className="block mb-1">Github Link:</label>
                            <input
                                type="url"
                                name="githubLink"
                                value={formData.githubLink}
                                onChange={handleChange}
                                className="w-full p-2 border rounded bg-amber-50"
                            />
                        </div>
                    </div>
                </section>

                <section>
                    <h2 className="text-xl font-semibold mb-4">Education</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label className="block mb-1">College: *</label>
                            <input
                                type="text"
                                name="college"
                                value={formData.college}
                                onChange={handleChange}
                                required
                                className="w-full p-2 border rounded bg-amber-50"
                            />
                        </div>
                        <div>
                            <label className="block mb-1">Major/Concentration: *</label>
                            <input
                                type="text"
                                name="majorConcentration"
                                value={formData.majorConcentration}
                                onChange={handleChange}
                                required
                                className="w-full p-2 border rounded bg-amber-50"
                            />
                        </div>
                        <div>
                            <label className="block mb-1">Second Major:</label>
                            <input
                                type="text"
                                name="secondMajor"
                                value={formData.secondMajor}
                                onChange={handleChange}
                                className="w-full p-2 border rounded bg-amber-50"
                            />
                        </div>
                        <div>
                            <label className="block mb-1">GPA:</label>
                            <input
                                type="text"
                                name="gpa"
                                value={formData.gpa}
                                onChange={handleChange}
                                className="w-full p-2 border rounded bg-amber-50"
                            />
                        </div>
                        <div>
                            <label className="block mb-1">Location of College: *</label>
                            <input
                                type="text"
                                name="locationOfCollege"
                                value={formData.locationOfCollege}
                                onChange={handleChange}
                                required
                                className="w-full p-2 border rounded bg-amber-50"
                            />
                        </div>
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
                                />
                            </div>
                        </div>
                        <div className="col-span-2">
                            <label className="block mb-1">Relevant Coursework:</label>
                            <textarea
                                name="relevantCoursework"
                                value={formData.relevantCoursework}
                                onChange={handleChange}
                                className="w-full p-2 border rounded bg-amber-50"
                                rows="3"
                            ></textarea>
                        </div>
                    </div>
                </section>

                <section>
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
                </section>

                <div className="text-center">
                    <button type="submit" className="bg-amber-500 text-white px-6 py-2 rounded hover:bg-amber-600 transition-colors">
                        Submit
                    </button>
                </div>
            </form>
        </div>
    );
};

export default ResumeQuestionnaire;
