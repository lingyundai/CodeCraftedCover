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
    resume=""
    # Create a prompt to extract relevant personal information according to the job description
    relevant_info=cortex.Complete('snowflake-arctic', f"Extract relevant personal information according to the job description from multiple resumes. The resumes:{st.session_state.fetched_data}, and job description:{st.session_state.job_description}",session = st.session_state.new_session)
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
