import dbConnection as dbConn
from snowflake.snowpark import Session
import streamlit as st
import snowflake.connector as snconn
import json
import snowflake.cortex as cortex 

def chatbot():
    instructions = "Be concise. Do not hallucinate"
    # st.write(st.session_state.job_description)
    # st.write(st.session_state.additional_info)
    # Initialize message history in session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                'role': 'assistant',
                'content': "Hello! I'm here to help you generate a cover letter. Please upload files and provide job description to get started."
                # 'content': st.session_state.fetched_data if len(st.session_state.fetched_data) > 0 else "No files uploaded yet. Please upload files to generate cover letter."
            }
        ]
    # User input prompt
    prompt = st.chat_input("Type your message", key="chat_input")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.isFirstPrompt = True

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):  
            context = ",".join(f"role:{message['role']} content:{message['content']}" for message in st.session_state.messages)
            response = cortex.Complete('mistral-large', f"Instructions:{instructions}, context:{context}, Prompt:{prompt}",session = st.session_state.new_session)
            st.markdown(response)

            st.session_state.messages.append({
                'role': 'assistant',
                'content': response
            })


        # Scroll to the last message
        st.write('<meta name="viewport" content="width=device-width, initial-scale=1">', unsafe_allow_html=True)
        st.write('<script>var element = document.body; element.scrollTop = element.scrollHeight;</script>', unsafe_allow_html=True)


def generate_cover_letter():
    # # Step 1: Extract relevant details from user data and job description
    st.write('Hello')
    personal_info = extract_personal_info()
    return

def extract_personal_info():
    resume = """
Name: John Doe
Email: johndoe@example.com
Phone: +1 (555) 123-4567
LinkedIn: linkedin.com/in/johndoe
GitHub: github.com/johndoe

Address:
1234 Elm Street
Tech City, CA 90210
United States

Objective:
Passionate and dedicated Software Developer with over 5 years of experience in full-stack development, seeking to leverage my expertise in software engineering to contribute to the success of a dynamic team.

Education:
Master of Science in Computer Science
Fictional University, Tech City, CA
August 2017 - May 2019
- GPA: 3.85/4.00
- Relevant coursework: Advanced Algorithms, Machine Learning, Distributed Systems

Bachelor of Science in Computer Science
Imaginary Institute of Technology, Tech City, CA
August 2013 - May 2017
- GPA: 3.75/4.00
- Relevant coursework: Data Structures, Database Systems, Operating Systems

Skills:
- Languages: Python, JavaScript, Java, C++
- Frameworks: React.js, Node.js, Angular, Spring Boot
- Databases: MySQL, PostgreSQL, MongoDB
- Tools: Git, Docker, Jenkins, Kubernetes
- Technologies: AWS, RESTful APIs, Microservices, Agile/Scrum

Professional Experience:
Software Developer
Tech Innovators Inc., Tech City, CA
July 2019 - Present
- Designed and developed scalable web applications using React.js and Node.js, improving user engagement by 25%.
- Implemented RESTful APIs and microservices architecture, enhancing system performance and maintainability.
- Collaborated with cross-functional teams to deliver new features and resolve critical bugs, ensuring timely releases.
- Mentored junior developers, providing guidance and support to enhance their coding skills and productivity.
- Utilized Docker and Kubernetes for containerization and orchestration, improving deployment efficiency.

Junior Software Developer
Creative Solutions, Tech City, CA
June 2017 - June 2019
- Assisted in the development of web applications using Java and Spring Boot, contributing to an increase in user satisfaction by 20%.
- Developed and maintained SQL and NoSQL databases, optimizing query performance and data retrieval times.
- Participated in Agile development processes, including sprint planning, stand-ups, and retrospectives.
- Conducted code reviews and collaborated with senior developers to ensure high-quality code standards.
- Created detailed technical documentation and user manuals for newly developed features and applications.

Projects:
E-commerce Platform Development
- Developed a full-stack e-commerce platform using React.js and Node.js, facilitating seamless online shopping experiences.
- Implemented payment gateway integration and user authentication, ensuring secure transactions and user data protection.
- Utilized MongoDB for database management, achieving efficient data storage and retrieval.

Machine Learning Model for Predictive Analysis
- Designed and trained machine learning models using Python and Scikit-learn to predict customer churn with 85% accuracy.
- Analyzed large datasets and performed feature engineering to enhance model performance and reliability.

Certifications:
- Certified Kubernetes Administrator (CKA)
- AWS Certified Solutions Architect – Associate
- Professional Scrum Master (PSM I)

References: Available upon request.
"""
    # Create a prompt to extract relevant personal information according to the job description
    relevant_info=cortex.Complete('snowflake-arctic', f"Extract relevant personal information according to the job description. The resumes:{st.session_state.fetched_data}, and job description:{st.session_state.job_description}",session = st.session_state.new_session)
    st.write(relevant_info)

# def extract_skills_experience(user_data):
#     # Extract skills and experience logic here
#     return user_data['skills'], user_data['experience']

# def generate_personal_profile(personal_info):
#     # Use Snowflake Arctic to generate personal profile
#     return f"Dear Hiring Manager,\n\nMy name is {personal_info[0]}..."

# def generate_experience_mapping(skills, experience, job_description):
#     # Use Snowflake Arctic to map skills and experience
#     return f"Based on your job description, I have the following relevant experience..."

# def address_gaps(skills, job_description):
#     # Identify and address gaps
#     return "While my experience does not directly include..., I have demonstrated..."

# def generate_conclusion(personal_info):
#     # Generate concluding paragraph
#     return "Thank you for considering my application..."

# f"Given the applicant's resume and the job description, generate a cover letter that includes the following sections: \n\n"
# f"1. Personal Profile Building Story: Introduce the applicant and highlight their core strengths and unique qualities. \n\n"
# f"2. Experience Mapping: Link the applicant's experiences and skills to the job description. Use scenarios to demonstrate impact. \n\n"
# f"3. Address Gaps: If there are gaps between the resume and job description, acknowledge and explain them. \n\n"
# f"4. Conclusion: Summarize the applicant's suitability for the role and express enthusiasm for the position. \n\n"
# f"Resume: {resume_data}\n\n"
# f"Job Description: {job_description}\n\n"
# f"Cover Letter:"
