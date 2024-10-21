# app/resume/routes.py

from flask import Blueprint, request, jsonify, current_app
import openai
#from openai.error import OpenAIError

resume_bp = Blueprint('resume', __name__)


def create_prompt(user_data):
    # Extract user data
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
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or another available model
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in generating resumes."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].message['content'].strip()

@resume_bp.route('/generate-resume', methods=['POST'])
def generate_resume():
    user_data = request.get_json()
    prompt = create_prompt(user_data)
    #try:
    generated_text = generate_resume_text(prompt)
    return jsonify({'generatedText': generated_text})
    #except openai.error.OpenAIError as e:
    #    current_app.logger.error(f'OpenAI API error: {e}')
    #    return jsonify({'error': 'Failed to generate text due to an API error.'}), 500
    #except Exception as e:
     #   current_app.logger.error(f'Unexpected error: {e}')
     #   return jsonify({'error': 'An unexpected error occurred.'}), 500