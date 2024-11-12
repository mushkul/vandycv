# app/resume/routes.py

import uuid
import os
import subprocess
from dotenv import load_dotenv
from flask import Flask, request, send_file, render_template_string, redirect, send_from_directory, url_for
from flask import Blueprint, request, jsonify, current_app
from openai import OpenAI
from firebase_admin import auth
from app.db import get_db_connection
os.environ["PATH"] += os.pathsep + "/opt/render/project/src/server"
# from openai.error import OpenAIError

resume_bp = Blueprint('resume_bp', __name__)

TEST = False


def test(out: str):
    print(out)


def create_prompt(user_data):
    print("Started prompt creation")
    first_name = user_data.get('firstName', '')
    middle_initial = user_data.get('middleInitial', '')
    last_name = user_data.get('lastName', '')
    address = user_data.get('address', '')
    email = user_data.get('email', '')
    contact_number = user_data.get('contactNumber', '')
    linkedin_link = user_data.get('linkedinLink', '')
    github_link = user_data.get('githubLink', '')
    college = user_data.get('college', '')
    major_concentration = user_data.get('majorConcentration', '')
    second_major = user_data.get('secondMajor', '')
    gpa = user_data.get('gpa', '')
    location_of_college = user_data.get('locationOfCollege', '')
    start_year = user_data.get('startYear', '')
    end_year = user_data.get('endYear', '')
    relevant_coursework = user_data.get('relevantCoursework', '')
    job_experiences = user_data.get('jobExperiences', [])

    # Build the prompt
    # print("\n\n", "name:", first_name, "\n\n\n")
    # exit(0)
    prompt = f"""
    You are a professional resume writer. Based on the following user information, generate the content for a professional resume. Provide:\n
    1. A compelling professional summary highlighting the user's qualifications, skills, and career objectives.\n
    2. An education section detailing the user's academic background.\n
    3. For each job experience, craft bullet points that emphasize responsibilities, achievements, and skills demonstrated.\n
    User Information:\n
    **Personal Details:**\n
    - **Name:** {first_name} {middle_initial} {last_name}\n
    - **Address:** {address}\n
    - **Email:** {email}\n
    - **Contact Number:** {contact_number}\n"""

    if linkedin_link:
        prompt += f"- **LinkedIn:** {linkedin_link}\n"
    if github_link:
        prompt += f"- **GitHub:** {github_link}\n"

    prompt += f"""**Education:**\n
    - **College:** {college}\n
    - **Major/Concentration:** {major_concentration}\n"""

    if second_major:
        prompt += f"- **Second Major:** {second_major}\n"
    if gpa:
        prompt += f"- **GPA:** {gpa}\n"

    prompt += f"- **Location:** {location_of_college}\n"
    prompt += f"- **Start Year:** {start_year}\n"
    prompt += f"- **End Year:** {end_year}\n"

    if relevant_coursework:
        prompt += f"- **Relevant Coursework:** {relevant_coursework}\n"

    prompt += "\n**Job Experiences:**\n"

    for idx, exp in enumerate(job_experiences):
        name = exp.get('name', '')
        title = exp.get('title', '')
        location = exp.get('location', '')
        description = exp.get('description', '')

        prompt += f"""
        **Job #{idx + 1}:**\n
        - **Company Name:** {name}\n
        - **Title:** {title}\n
        - **Location:** {location}\n
        - **Description:** {description}\n
        """

    prompt += """
    Instructions:
    - Use a professional and engaging tone suitable for a resume.
    - The professional summary should be 2-3 sentences.
    - For job experiences, provide 3-5 bullet points focusing on achievements and responsibilities.
    - Highlight any skills, technologies, or tools relevant to the user's field.
    - Do not include any placeholders or mentions of missing information.
    - Provide the output in plain text without any markdown formatting.
    """

    return prompt


def generate_resume_text(prompt):
    if not TEST:
        print("GENERATED2")

        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or another available model
            messages=[
                {"role": "system", "content": "You are a helpful assistant specialized in generating resumes."},
                {"role": "user", "content": prompt}
            ]
            # , key = openai.key
        )
        print("GENERATED3")
        print("Response", response)
        return response.choices[0].message.content.strip()
    else:
        return "It is Adam from Vanderbilt. 4.0 GPA and amazing work experience.\nExperience #1\nExperience #2\n"


@resume_bp.route('/generateresume/', methods=['POST'])
def generate_resume():
    with open("cv.tex", 'r') as file:
        latex_content = file.read()
    print(latex_content)
    # return redirect(url_for('resume_bp.generate_pdf', latex_content=latex_content))
    # return jsonify({'generatedText': "HI"})
    try:

        # Get the ID token from the Authorization header
        id_token = None
        auth_header = request.headers.get('Authorization', None)
        if auth_header:
            # The header is of the form 'Bearer <token>'
            id_token = auth_header.split(' ')[1]

        if id_token is None:
            return jsonify({'error': 'Unauthorized'}), 401

        # Verify the ID token
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        user_data = request.get_json()
        print("User data received:", user_data)
        # Extract user data
        first_name = user_data.get('firstName', '')
        last_name = user_data.get('lastName', '')
        middle_initial = user_data.get('middleInitial', '')
        address = user_data.get('address', '')
        email = user_data.get('email', '')
        contact_number = user_data.get('contactNumber', '')
        linkedin_link = user_data.get('linkedinLink', '')
        github_link = user_data.get('githubLink', '')
        college = user_data.get('college', '')
        major_concentration = user_data.get('majorConcentration', '')
        second_major = user_data.get('secondMajor', '')
        gpa = user_data.get('gpa', '')
        location_of_college = user_data.get('locationOfCollege', '')
        start_year = user_data.get('startYear', '')
        end_year = user_data.get('endYear', '')
        relevant_coursework = user_data.get('relevantCoursework', '')
        job_experiences = user_data.get('jobExperiences', [])

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Begin transaction
            conn.autocommit = False

            # Insert into questionnaires
            insert_questionnaire_query = """
                INSERT INTO questionnaires (
                    uid, name, first_name, last_name, middle_initial, address, email, contact_number,
                    linkedin_link, github_link, college, major_concentration, second_major, gpa,
                    location_of_college, start_year, end_year, relevant_coursework
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                ) RETURNING questionnaire_id;
            """

            insert_questionnaire_values = (
                uid,
                'Resume Questionnaire',
                first_name,
                last_name,
                middle_initial,
                address,
                email,
                contact_number,
                linkedin_link,
                github_link,
                college,
                major_concentration,
                second_major,
                gpa,
                location_of_college,
                start_year,
                end_year,
                relevant_coursework
            )

            cursor.execute(insert_questionnaire_query,
                           insert_questionnaire_values)
            questionnaire_id = cursor.fetchone()[0]

            # Insert job experiences
            insert_experience_query = """
                INSERT INTO job_experiences (
                    questionnaire_id, name, title, location, description
                ) VALUES (
                    %s, %s, %s, %s, %s
                );
            """

            for exp in job_experiences:
                name = exp.get('name', '')
                title = exp.get('title', '')
                location = exp.get('location', '')
                description = exp.get('description', '')

                cursor.execute(insert_experience_query, (
                    questionnaire_id,
                    name,
                    title,
                    location,
                    description
                ))

            # Commit transaction
            conn.commit()

        except Exception as e:
            conn.rollback()
            current_app.logger.error(f'Database error: {e}')
            return jsonify({'error': 'Database error occurred'}), 500
        finally:
            cursor.close()
            conn.close()
            print("HELLO")
            return generate_pdf(uid, questionnaire_id, latex_content)

        # Optionally, generate the resume text
        prompt = create_prompt(user_data)
        generated_text = generate_resume_text(prompt)

        # Return the generated text to the frontend
        return jsonify({'generatedText': generated_text})

    except Exception as e:
        current_app.logger.error(f'Unexpected error: {e}')
        return jsonify({'error': 'An unexpected error occurred.'}), 500


# Temporary directory to store PDF files
load_dotenv()
TEMP_DIR = os.getenv("PERSISTENT_ADDRESS")
# os.makedirs(TEMP_DIR, exist_ok=True)


# @resume_bp.route('/generate_pdf')
def generate_pdf(uid, questionnaire_id, latex_content):
    print("PERSISTENT_ADDRESS", TEMP_DIR)
    # latex_content = request.json.get("latex_content")
    if not latex_content:
        return {"error": "No LaTeX content provided"}, 400

    pdf_id = f"{uid}_{questionnaire_id}"
    print("making dir")
    os.makedirs(TEMP_DIR, exist_ok=True)
    print("made dir")
    tex_file_path = os.path.join(TEMP_DIR, f"{pdf_id}.tex")
    pdf_file_path = os.path.join(TEMP_DIR, f"{pdf_id}.pdf")

    with open(tex_file_path, "w") as tex_file:
        tex_file.write(latex_content)

    try:
        subprocess.run(["tectonic", "-o", TEMP_DIR, tex_file_path],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        return {"error": "Failed to generate PDF", "details": e.stderr.decode()}, 500

    return view_pdf(pdf_id)
# redirect(url_for('view_pdf', pdf_id=pdf_id))


# @resume_bp.route('/view_pdf/<pdf_id>')
def view_pdf(pdf_id):
    pdf_file_path = os.path.join(TEMP_DIR, f"{pdf_id}.pdf")
    if not os.path.exists(pdf_file_path):
        return {"error": "PDF not found"}, 404

    html_content = f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>View PDF</title>
      </head>
      <body>
        <h1>Generated PDF</h1>
        <embed src="{url_for('resume_bp.get_pdf', pdf_id=pdf_id)}" type="application/pdf" width="100%" height="100%"/>
      </body>
    </html>
    """

    print(html_content)
    return redirect(url_for('resume_bp.get_pdf', pdf_id=pdf_id))
    # return render_template_string(html_content)


@resume_bp.route('/pdf/<pdf_id>')
def get_pdf(pdf_id):
    pdf_file_path = os.path.join(TEMP_DIR, f"{pdf_id}.pdf")
    if not os.path.exists(pdf_file_path):
        return {"error": "PDF not found"}, 404

    return send_file(pdf_file_path, as_attachment=False)


@resume_bp.route('/pdfs/<uid>/<questionnaire_id>', methods=['GET'])
def get_pdf1(uid, questionnaire_id):
    return send_file(os.path.join(TEMP_DIR, f"{uid}_{questionnaire_id}.pdf"))
