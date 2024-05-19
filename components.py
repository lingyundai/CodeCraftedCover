import streamlit as st

import pandas as pd
from io import StringIO, BytesIO
from PyPDF2 import PdfReader
from docx import Document
import snowflake.cortex as cortex 


def title():
    st.title("Generate Cover Letter", anchor=False)
    st.subheader("That Actually Works.")

def app_introduction():
    st.caption("Many cover letter generators take minimal information and generate a terrible cover letter that")
    st.caption("1. Obviously is generated with AI - robotic words, inaccurate information.")
    st.caption("2. Provide no substantial information that hiring manager wants to see - repetitive content, too generalized.")
    st.caption("Result In 'Unfortunately...' e-mails, bad impression, frustration, time wasted for both parties.")
    st.caption("This application will fix that!! Hopefully. In these ways -")
    st.caption("1. We use comprehensive information to generate a detailed, useful cover letter for the job type you are applying to.")
    st.caption("2. We keep history of the files you uploaded, overtime, the cover letter just gets more and more personalized for you and your desired job type.")
    st.caption("3. Chat GPT? NO! We use the newest LLM technology 'Snowflake Arctic' that generates high-quality models.")
    st.caption("In the end, we are in this together. Happy generating!")

def connection_parameters_input():
    account = st.sidebar.text_input('Enter Snowflake Account', 
                                    placeholder="Your Snowflake account",
                                    help="One of the Snowflake commercial regions, besides us-east as our LLM is not currently avaliable in those regions." ,value = st.secrets["account"])
    username = st.sidebar.text_input('Enter Snowflake Username', placeholder="Your Snowflake username" ,value = st.secrets["username"])
    password = st.sidebar.text_input('Enter Snowflake Password', placeholder="Your Snowflake password", type='password', value = st.secrets["password"])
    submit = st.sidebar.button("Connect")
    return account, username, password, submit


def job_type_select(job_type_list):
    job_type = st.sidebar.selectbox(
        "Select Job Type", 
        job_type_list.values(),
        help="This will help us to create designated chats for you.")
    return job_type


def job_description_input():
    st.sidebar.text_area("Enter Job Description", 
                         placeholder="Copy-and-paste the job description, the more information the better!")
    if st.sidebar.button("Submit"):
        st.sidebar.caption("Successfully Submitted!")

def addtional_info_input():
    st.sidebar.text_area("Anything Else That Would Help?", 
                 placeholder="For example, 'please do not copy and paste things from job description to the cover letter!' or 'I am also experienced in xxx'.")

def generate_button():
    # Use columns to keep button to the right of the side bar
    col1, col2 = st.sidebar.columns([0.7, 0.4])
    col2.button("Ready to Generate  ➡️")

def chatbot():
    instructions = "Be concise. Do not hallucinate"

    # Initialize message history in session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                'role': 'assistant',
                'content': st.session_state.fetched_data if len(st.session_state.fetched_data) > 0 else "No files uploaded yet. Please upload files to generate cover letter."
            }
        ]
    # User input prompt
    prompt = st.chat_input("Type your message", key="chat_input")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

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