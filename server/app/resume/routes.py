
# app/resume/routes.py


import re
from jinja2 import Template
import uuid
import os
import subprocess
import json
from dotenv import load_dotenv
from flask import Flask, request, send_file, render_template_string, redirect, send_from_directory, url_for
from flask import Blueprint, request, jsonify, current_app
from openai import OpenAI
from firebase_admin import auth
from app.db import get_db_connection
os.environ["PATH"] += os.pathsep + "/opt/render/project/src/server"

# from openai.error import OpenAIError

# for testing purposes

resume_bp = Blueprint('resume_bp', __name__)
load_dotenv()
TEMP_DIR = os.getenv("PERSISTENT_ADDRESS")
if TEMP_DIR is None:
    TEMP_DIR = "/files/"
TEST = False


def escape_latex(s):
    if not isinstance(s, str):
        return s

    # Map special characters to their escaped versions
    special_chars = {
        '\\': r'\textbackslash{}',
        '{': r'\{',
        '}': r'\}',
        '#': r'\#',
        '$': r'\$',
        '%': r'\%',
        '&': r'\&',
        '_': r'\_',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
    }

    # Create a regex pattern to find any of the special characters
    pattern = re.compile('|'.join(re.escape(char)
                         for char in special_chars.keys()))

    # Replace each special character with its escaped version
    return pattern.sub(lambda match: special_chars[match.group()], s)


def escape_user_data(data):
    if isinstance(data, dict):
        return {k: escape_user_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [escape_user_data(item) for item in data]
    else:
        return escape_latex(data)


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
    job_description_details = user_data.get('jobDescriptionDetails', '')
    interests = user_data.get('interests', '')
    tech_stack = user_data.get('techStack', '')
    language_skills = user_data.get('languageSkills', [])

    # Build the prompt
    prompt = f"""
        You are a professional resume writer. Based on the following user information, generate the content for a professional resume. Provide:

        1. A compelling professional summary highlighting the user's qualifications, skills, and career objectives.
        2. An education section detailing the user's academic background.
        3. For each job experience, craft bullet points that emphasize responsibilities, achievements, and skills demonstrated.
        4. Determine the best order for the job experiences to maximize the user's qualifications.
        5. Ensure that the bullet points for each job experience are based on the user's job descriptions and the overall job description details.

        User Information:

        **Personal Details:**
        - **Name:** {first_name} {middle_initial} {last_name}
        - **Address:** {address}
        - **Email:** {email}
        - **Contact Number:** {contact_number}
        """
    if linkedin_link:
        prompt += f"- **LinkedIn:** {linkedin_link}\n"
    if github_link:
        prompt += f"- **GitHub:** {github_link}\n"

    prompt += f"""
        **Education:**
        - **College:** {college}
        - **Major/Concentration:** {major_concentration}
        """

    if second_major:
        prompt += f"- **Second Major:** {second_major}\n"
    if gpa:
        prompt += f"- **GPA:** {gpa}\n"

    prompt += f"- **Location:** {location_of_college}\n"
    prompt += f"- **Start Year:** {start_year}\n"
    prompt += f"- **End Year:** {end_year}\n"

    if relevant_coursework:
        prompt += f"- **Relevant Coursework:** {relevant_coursework}\n"

    if tech_stack:
        prompt += f"- **Tech Stack:** {tech_stack}\n"
    if interests:
        prompt += f"- **Interests:** {interests}\n"
    if language_skills:
        prompt += f"- **Language Skills:** {language_skills}\n"

    prompt += f"""
        **Job Description Details:**
        {job_description_details}

        **Job Experiences:**
        """

    for idx, exp in enumerate(job_experiences):
        company = exp.get('company', '')
        position = exp.get('position', '')
        location = exp.get('location', '')
        description = exp.get('description', '')
        start_year_exp = exp.get('startYear', '')
        end_year_exp = exp.get('endYear', '')

        prompt += f"""
        **Job #{idx + 1}:**
        - **Company:** {company}
        - **Position:** {position}
        - **Location:** {location}
        - **Description:** {description}
        - **Start Year:** {start_year_exp}
        - **End Year:** {end_year_exp}
        """

    prompt += """
        Instructions:
        - Use a professional and engaging tone suitable for a resume.
        - The professional summary should be 2-3 sentences.
        - For job experiences, provide 3-5 bullet points focusing on achievements and responsibilities.
        - Highlight any skills, technologies, or tools relevant to the user's field.
        - Determine the best order for the job experiences to maximize the user's qualifications.
        - Provide the output in JSON format as specified below.
        - Do not include any placeholders or mentions of missing information.

        Return Format (JSON):
        {
        "professionalSummary": "Your professional summary here.",
        "jobExperiences": [
            {
            "company": "Company Name",
            "position": "Position Title",
            "location": "Location",
            "startYear": "YYYY",
            "endYear": "YYYY",
            "bullets": [
                "First bullet point",
                "Second bullet point",
                "..."
            ]
            },
            {
            "company": "Next Company",
            "...": "...",
            "bullets": [
                "..."
            ]
            }
            // Add more job experiences as needed
        ]
        }
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


def generate_bullet_points_and_order(prompt):
    print("HERE", os.environ["OPENAI_API_KEY"])
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use the appropriate model
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500,
            n=1,
            stop=None,
        )

        assistant_message = response.choices[0].message.content.strip()
        print(assistant_message)
        return assistant_message

    except Exception as e:
        current_app.logger.error(
            f"Error generating bullet points and order: {e}", exc_info=True)
        return None


def process_chatgpt_response(chatgpt_response, user_data):
    if not chatgpt_response:
        # If there's an error or no response, return the original job experiences
        return user_data.get('jobExperiences', [])

    try:
        # Extract JSON from the response
        json_start = chatgpt_response.find('{')
        json_end = chatgpt_response.rfind('}') + 1
        json_data = chatgpt_response[json_start:json_end]

        data = json.loads(json_data)

        # Escape job experiences
        job_experiences = data.get('jobExperiences', [])

        for job in job_experiences:
            job['company'] = escape_latex(job.get('company', ''))
            job['position'] = escape_latex(job.get('position', ''))
            job['location'] = escape_latex(job.get('location', ''))
            job['startYear'] = escape_latex(job.get('startYear', ''))
            job['endYear'] = escape_latex(job.get('endYear', ''))
            # Escape bullets
            job['bullets'] = [escape_latex(bullet)
                              for bullet in job.get('bullets', [])]

        return job_experiences

    except json.JSONDecodeError as e:
        current_app.logger.error(f"JSON decoding error: {e}", exc_info=True)
        # If there's an error parsing the response, return the original job experiences
        return user_data.get('jobExperiences', [])


@resume_bp.route('/generateresume/', methods=['POST'])
def generate_resume():

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
        job_description_details = user_data.get('jobDescriptionDetails', '')
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
        language_skills = user_data.get('languageSkills', [])  # List of dicts
        tech_stack = user_data.get('techStack', '')  # Comma-separated string
        interests = user_data.get('interests', '')  # Comma-separated string

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

            insert_experience_query = """
                INSERT INTO job_experiences (
                    questionnaire_id, company, position, location, description, start_year, end_year
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s
                );
            """

            for exp in job_experiences:
                company = exp.get('company', '')
                position = exp.get('position', '')
                location = exp.get('location', '')
                description = exp.get('description', '')
                start_year = exp.get('startYear', '')
                end_year = exp.get('endYear', '')

                cursor.execute(insert_experience_query, (
                    questionnaire_id,
                    company,
                    position,
                    location,
                    description,
                    start_year,
                    end_year
                ))

            insert_language_skill_query = """
                INSERT INTO language_skills (
                    questionnaire_id, language, proficiency
                ) VALUES (%s, %s, %s);
            """

            for lang_skill in language_skills:
                language = lang_skill.get('language', '')
                proficiency = lang_skill.get('proficiency', '')
                cursor.execute(insert_language_skill_query, (
                    questionnaire_id, language, proficiency
                ))

            tech_stack_list = [tech.strip()
                               for tech in tech_stack.split(',') if tech.strip()]
            insert_tech_stack_query = """
                INSERT INTO tech_stacks (
                    questionnaire_id, tech
                ) VALUES (%s, %s);
            """

            for tech in tech_stack_list:
                cursor.execute(insert_tech_stack_query, (
                    questionnaire_id, tech
                ))

            interests_list = [interest.strip()
                              for interest in interests.split(',') if interest.strip()]
            insert_interest_query = """
                INSERT INTO interests (
                    questionnaire_id, interest
                ) VALUES (%s, %s);
            """

            for interest in interests_list:
                cursor.execute(insert_interest_query, (
                    questionnaire_id, interest
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

        # Create the prompt
        prompt = create_prompt(user_data)

        # Generate bullet points and order
        chatgpt_response = generate_bullet_points_and_order(prompt)

        # Process the response
        ordered_job_experiences = process_chatgpt_response(
            chatgpt_response, job_experiences)

        # Escape user data
        escaped_user_data = escape_user_data(user_data)

        # Replace job experiences with the ordered ones
        escaped_user_data['jobExperiences'] = ordered_job_experiences

        # Read the LaTeX template
        with open("cv.tex", 'r') as file:
            latex_template = file.read()

        # Render the template with escaped user data
        template = Template(latex_template)
        rendered_latex = template.render(**escaped_user_data)

        # Generate PDF
        # Generate PDF and get the file path
        pdf_file_path = generate_pdf(uid, questionnaire_id, rendered_latex)

        # Return JSON response with questionnaire_id
        return jsonify({'questionnaire_id': questionnaire_id})

        # Optionally, generate the resume text
        # prompt = create_prompt(user_data)
        # generated_text = generate_resume_text(prompt)

        # Return the generated text to the frontend
        # return jsonify({'generatedText': generated_text})

    except Exception as e:
        current_app.logger.error(f'Unexpected error: {e}')
        return jsonify({'error': 'An unexpected error occurred.'}), 500


# Temporary directory to store PDF files

# os.makedirs(TEMP_DIR, exist_ok=True)


# @resume_bp.route('/generate_pdf')
def generate_pdf(uid, questionnaire_id, latex_content):
    global TEMP_DIR
    TEMP_DIR = os.getenv("PERSISTENT_ADDRESS")
    TECTONIC_ADDRESS = "tectonic"
    if TEMP_DIR is None:
        TEMP_DIR = "/files/"
        TECTONIC_ADDRESS = "../tectonic"
    print("PERSISTENT_ADDRESS", TEMP_DIR)
    # latex_content = request.json.get("latex_content")
    if not latex_content:
        return {"error": "No LaTeX content provided"}, 400

    pdf_id = f"{uid}_{questionnaire_id}"
    os.makedirs(TEMP_DIR, exist_ok=True)
    tex_file_path = os.path.join(TEMP_DIR, f"{pdf_id}.tex")
    pdf_file_path = os.path.join(TEMP_DIR, f"{pdf_id}.pdf")

    with open(tex_file_path, "w") as tex_file:
        tex_file.write(latex_content)
    print("LaTeX file written to:", tex_file_path)
    try:
        # print(TEMP_DIR, tex_file_path)
        subprocess.run([TECTONIC_ADDRESS, "-o", TEMP_DIR, tex_file_path],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("PDF generated at:", pdf_file_path)

    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode()
        print("Error during PDF generation:", error_message)
        return {"error": "Failed to generate PDF", "details": error_message}, 500

    return view_pdf(pdf_id)
# redirect(url_for('view_pdf', pdf_id=pdf_id))


# @resume_bp.route('/view_pdf/<pdf_id>')
def view_pdf(pdf_id):
    print("got to view pdf")
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

    # print(html_content)
    print("File PATH2", pdf_file_path)
    print("URL:", url_for('resume_bp.get_pdf', pdf_id=pdf_id))
    return redirect(url_for('resume_bp.get_pdf', pdf_id=pdf_id))
    # return render_template_string(html_content)


@resume_bp.route('/pdf/<pdf_id>')
def get_pdf(pdf_id):
    # pdf_file_path = "{pdf_file_path}"
    pdf_file_path = os.path.join(TEMP_DIR, f"{pdf_id}.pdf")
    print("FILE PATH", pdf_file_path)
    if not os.path.exists(pdf_file_path):
        return {"error": "PDF not found"}, 404

    return send_file(pdf_file_path, as_attachment=False)


@resume_bp.route('/pdfs/<uid>/<questionnaire_id>', methods=['GET'])
def get_pdf1(uid, questionnaire_id):
    load_dotenv()
    TEMP_DIR = os.getenv("PERSISTENT_ADDRESS")
    if TEMP_DIR is None:
        TEMP_DIR = "/files/"
    print(TEMP_DIR)
    print(uid)
    print(questionnaire_id)
    return send_file(os.path.join(TEMP_DIR, f"{uid}_{questionnaire_id}.pdf"))


@resume_bp.route('/resumes/', methods=['GET'])
def get_resumes():
    try:
        # Step 1: Authenticate the user
        id_token = None
        auth_header = request.headers.get('Authorization', None)
        if auth_header:
            id_token = auth_header.split(' ')[1]
        if id_token is None:
            return jsonify({'error': 'Unauthorized'}), 401
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        # Step 2: Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Step 3: Query for the user's resumes
        select_questionnaires_query = """
            SELECT questionnaire_id, name, date_created
            FROM questionnaires
            WHERE uid = %s
            ORDER BY date_created DESC;
        """
        cursor.execute(select_questionnaires_query, (uid,))
        questionnaires = cursor.fetchall()

        # Step 4: Format the data
        resumes_list = []
        for q in questionnaires:
            questionnaire_id = q[0]
            name = q[1]
            date_created = q[2]
            if date_created:
                date_created_str = date_created.strftime('%Y-%m-%d %H:%M')
            else:
                date_created_str = 'Unknown'
            resumes_list.append({
                'questionnaire_id': questionnaire_id,
                'name': name,
                'date_created': date_created_str
            })

        # Step 5: Return the data as JSON
        return jsonify({'resumes': resumes_list})

    except Exception as e:
        current_app.logger.error(f'Error fetching resumes: {e}', exc_info=True)
        return jsonify({'error': 'An error occurred while fetching resumes.'}), 500
