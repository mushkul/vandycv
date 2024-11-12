
# app/resume/routes.py

from jinja2 import Template
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

#for testing purposes

resume_bp = Blueprint('resume_bp', __name__)
load_dotenv()
TEMP_DIR = os.getenv("PERSISTENT_ADDRESS")
if TEMP_DIR is None:
    TEMP_DIR = "/files/"
TEST = False

def escape_latex(s):
    if isinstance(s, str):
        return s.replace('\\', r'\textbackslash{}') \
                .replace('&', r'\&') \
                .replace('%', r'\%') \
                .replace('$', r'\$') \
                .replace('#', r'\#') \
                .replace('_', r'\_') \
                .replace('{', r'\{') \
                .replace('}', r'\}') \
                .replace('~', r'\textasciitilde{}') \
                .replace('^', r'\^{}')
    return s

def escape_user_data(data):
    if isinstance(data, dict):
        return {k: escape_user_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [escape_user_data(item) for item in data]
    else:
        return escape_latex(data)

def test(out: str):
    print(out)


def escape_latex(s):
    if isinstance(s, str):
        return s.replace('\\', r'\textbackslash{}') \
                .replace('&', r'\&') \
                .replace('%', r'\%') \
                .replace('$', r'\$') \
                .replace('#', r'\#') \
                .replace('_', r'\_') \
                .replace('{', r'\{') \
                .replace('}', r'\}') \
                .replace('~', r'\textasciitilde{}') \
                .replace('^', r'\^{}')
    return s


def escape_user_data(data):
    if isinstance(data, dict):
        return {k: escape_user_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [escape_user_data(item) for item in data]
    else:
        return escape_latex(data)


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
        # Escape user data and process job descriptions
        escaped_user_data = escape_user_data(user_data)

        # Process job descriptions into bullets
        for job in escaped_user_data.get('jobExperiences', []):
            job['bullets'] = job.get('description', '').split('\n')

        # Optionally, you can add a 'professionalSummary' field if you want
        # escaped_user_data['professionalSummary'] = generate_professional_summary(user_data)

        # Read the LaTeX template
        with open("cv.tex", 'r') as file:
            latex_template = file.read()

        # Render the template with escaped user data
        template = Template(latex_template)
        rendered_latex = template.render(**escaped_user_data)

        # Generate PDF
        return generate_pdf(uid, questionnaire_id, rendered_latex)

        # Optionally, generate the resume text
        #prompt = create_prompt(user_data)
        #generated_text = generate_resume_text(prompt)

        # Return the generated text to the frontend
        #return jsonify({'generatedText': generated_text})

    except Exception as e:
        current_app.logger.error(f'Unexpected error: {e}')
        return jsonify({'error': 'An unexpected error occurred.'}), 500


# Temporary directory to store PDF files

# os.makedirs(TEMP_DIR, exist_ok=True)


# @resume_bp.route('/generate_pdf')
def generate_pdf(uid, questionnaire_id, latex_content):
    global TEMP_DIR
    TEMP_DIR = os.getenv("PERSISTENT_ADDRESS")
    if TEMP_DIR is None:
        TEMP_DIR = "/files/"
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
        subprocess.run(["tectonic", "-o", TEMP_DIR, tex_file_path],
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
                date_created_str = date_created.strftime('%Y-%m-%d %H-%M')
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

