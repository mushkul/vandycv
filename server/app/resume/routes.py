# app/resume/routes.py

from flask import Blueprint, request, jsonify, current_app
from openai import OpenAI
from firebase_admin import auth
from app.db import get_db_connection

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

            cursor.execute(insert_questionnaire_query, insert_questionnaire_values)
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

        # Optionally, generate the resume text
        prompt = create_prompt(user_data)
        generated_text = generate_resume_text(prompt)

        # Return the generated text to the frontend
        return jsonify({'generatedText': generated_text})

    except Exception as e:
        current_app.logger.error(f'Unexpected error: {e}')
        return jsonify({'error': 'An unexpected error occurred.'}), 500