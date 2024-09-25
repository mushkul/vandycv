# VandyCV - Resume Builder for Vanderbilt Students

## Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Features](#features)
- [Technologies](#technologies)
- [Setup Instructions](#setup-instructions)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

VandyCV is a web-based software application designed to help Vanderbilt University students create personalized resumes tailored to their academic majors and career goals. With the integration of customizable templates and AI-assisted content generation, VandyCV streamlines the resume creation process, allowing students to present their qualifications effectively to potential employers or graduate programs.

## Problem Statement

Many students struggle with creating resumes that highlight their skills and experiences in a way that is industry-specific or tailored to the requirements of different academic majors. Generic resume templates often fail to adequately showcase a student’s qualifications, leading to less impactful applications.

## Solution

VandyCV solves this issue by offering major-specific resume templates, an intuitive questionnaire to gather essential information, and AI-generated suggestions for work experiences and leadership roles. The platform also provides a dashboard for students to manage and track multiple resumes.

## Features

- **Major-Specific Resume Templates**: Pre-designed templates tailored to specific majors.
- **AI-Assisted Content Generation**: AI-generated descriptions for work experiences and leadership roles.
- **Resume Management**: A dashboard to manage, track, and customize multiple resumes.
- **Export to PDF**: Users can download their resumes in PDF format.
- **Drag-and-Drop Interface**: Allows users to easily customize their resumes.

## Technologies

- **Frontend**: Next.js with Tailwind CSS for easy styling.
- **Backend**: Flask for server-side logic.
- **Database**: PostgreSQL for storing user information and resume data.
- **AI Integration**: GPT API for generating professional descriptions.
- **Authentication**: Vanderbilt email authentication with potential Firebase integration.

## Setup Instructions

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-repo/VandyCV.git
   cd VandyCV
   ```

2. **Install dependencies**

   ```bash
   cd client
   npm install
   cd ../server
   python3 -m venv venv         # Create a virtual environment
   source venv/bin/activate      # Activate the virtual environment (macOS/Linux)
   venv\Scripts\activate         # Activate the virtual environment (Windows)
   pip install -r requirements.txt # install all requirement packages
   ```

3. **Start frontend app**:
   ```bash
   npm run dev
   ```
4. **Start backend app**:
   ```bash
   cd server
   source venv/bin/activate # Activate the virtual environment
   python3 server.py
   ```
