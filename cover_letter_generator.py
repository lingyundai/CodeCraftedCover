import streamlit as st
import snowflake.cortex as cortex 

import json

def chatbot():
    instructions = "Be concise. Do not hallucinate"
    # Initialize message history in session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                'role': 'assistant',
                'content': generate_initial_content() if len(st.session_state.fetched_data) > 0 
                else "No files uploaded yet. Please upload files to generate cover letter."
            }
        ]
    
    if st.session_state.isGenerated:
        initial_prompt = generate_initial_prompt()
        context = ",".join(f"role:{message['role']} content:{message['content']}" for message in st.session_state.messages)
        response = cortex.Complete('snowflake-arctic', f"Instructions:{instructions}, context:{context}, Prompt:{initial_prompt}", 
                                   session = st.session_state.new_session)
        st.markdown(response)

    # User input prompt
    prompt = st.chat_input("If you have any questions or need assistance, please type here.")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.isFirstPrompt = True

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):  
            context = ",".join(f"role:{message['role']} content:{message['content']}" for message in st.session_state.messages)
            response = cortex.Complete('snowflake-arctic', f"Instructions:{instructions}, context:{context}, Prompt:{prompt}", 
                                       session = st.session_state.new_session)
            st.markdown(response)

            st.session_state.messages.append({
                'role': 'assistant',
                'content': response
            })


        # Scroll to the last message
        st.write('<meta name="viewport" content="width=device-width, initial-scale=1">', unsafe_allow_html=True)
        st.write('<script>var element = document.body; element.scrollTop = element.scrollHeight;</script>', unsafe_allow_html=True)


def generate_initial_content():
    # return "Hello! I'm here to help you generate a cover letter. Please upload files and provide job description to get started."
    context = [
        "Generate cover letter Based on the uploaded files and provided ",
        f"Resume: {st.session_state.fetched_data}\n\n"
        f"Job Description: {st.session_state.job_description}\n\n"
        f"Additional Information: {st.session_state.additional_info}\n\n"
        ]
    return context

def generate_initial_prompt():
    prompt = [
        f"Given the applicant's resume and the job description, generate a cover letter that includes the following sections: \n\n"
        f"1. Personal Profile Building Story: Introduce the applicant and highlight their core strengths and unique qualities. \n\n"
        f"2. Experience Mapping: Link the applicant's experiences and skills to the job description. Use scenarios to demonstrate impact. \n\n"
        f"3. Address Gaps: If there are gaps between the resume and job description, acknowledge and explain them. \n\n"
        f"4. Conclusion: Summarize the applicant's suitability for the role and express enthusiasm for the position. \n\n"
    ]
    return prompt

def extract_personal_info(user_data, dbConnUserInfo):
    # Create a prompt to extract relevant personal information according to the job description
    prompt = [
        {
            'role': 'system',
            'content': 'You are a helpful AI assistant. Extract the relevant personal information from the user data according to the job description.'
        },
        {
            'role': 'user',
            'content': user_data
        }
    ]

    options = {
        'temperature': 0.7,
        'max_tokens': 10
    }
    # Define the parameters
    params = {
        'prompt': json.dumps(prompt),
        'options': json.dumps(options)
    }

    # Use Snowflake to generate relevant personal information
    cur = dbConnUserInfo.cursor()
    try:
        query="SELECT SNOWFLAKE.CORTEX.COMPLETE(%s, %s, %s)"
        cur.execute(query, ('snowflake-arctic', params['prompt'], params['options']))
        
        result = cur.fetchall()
        print(result)
        relevant_info = result[0][0] if result else ""
    finally:
        cur.close()

    return relevant_info
