import streamlit as st
from dbConnection import databaseConnection
from dbOperation import create_database, switch_database, create_table, insert_data, fetch_data
import pandas as pd
from io import StringIO, BytesIO
from PyPDF2 import PdfReader
from docx import Document
import constants as const



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


def file_upload(job_type):
    print(st.session_state)
    text = []
    uploaded_file = st.sidebar.file_uploader("Upload Files", 
                             type=["pdf", "docx"], 
                             help="Any file that you think would help us to generate a accurate cover letter for you",
                             accept_multiple_files=True)
    if uploaded_file is not None:
        text = []  # Initialize text as an empty list
        for file in uploaded_file:
            # To read file as bytes:
            bytes_data = file.read()
            file_content = ''  # Initialize file_content as an empty string

            if file.type == 'application/pdf':
                # Handle PDF files
                reader = PdfReader(BytesIO(bytes_data))
                for page in reader.pages:
                    file_content += page.extract_text() + ' '
            elif file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                # Handle DOCX files
                doc = Document(BytesIO(bytes_data))
                for para in doc.paragraphs:
                    file_content += para.text + ' '

            # Append a dictionary with the filename and file content to the text list
            text.append([{'file_name': file.name, 'file_content': file_content.strip()}])
            # print(text)
    
    con = databaseConnection(st.session_state.username, st.session_state.password , st.session_state.account)
    cur = con.cursor()
    switch_database(cur, 'USERDB')
    table_name = job_type.replace(' ', '_')
    create_table(cur, table_name)
    for data in text:
        insert_data(cur, table_name, data)
    con.close()

def job_description_input():
    st.sidebar.text_area("Enter Job Description", 
                         placeholder="Copy-and-paste the job description, the more information the better!")

def addtional_info_input():
    st.sidebar.text_area("Anything Else That Would Help?", 
                 placeholder="For example, 'please do not copy and paste things from job description to the cover letter!' or 'I am also experienced in xxx'.")

def submit_button():
    st.button("Generate")

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

def file_history(session_state, job_type):
    # Get the file history for the selected job type
    job_file_history = session_state.get(job_type, [])
    st.sidebar.write(f"File History For {job_type} Position:")
    # Display text based on if file history is empty
    if len(job_file_history) == 0:
        st.sidebar.write("No File Found")
    else:
        for file in job_file_history:
            # Styling the file and remove button
            col1, col2 = st.sidebar.columns([0.7, 0.2])
            col1.write(file)
            # if file removed remove from session state
            if col2.button("Remove", key=f"remove_{file}"):
                session_state[job_type].remove(file)
                # re-render
                st.rerun() 

def db_connect_error(error):
    st.sidebar.caption(f"{error}")

def db_connect_success(username, password, account):
    st.sidebar.caption("Successfully Connected!")
    if (username and password and account):
        # Connect to the database
        con = databaseConnection(username, password, account)

        # Create a cursor object
        cur = con.cursor()

        # Perform operations on the database
        create_database(cur, 'userDB')
        switch_database(cur, 'userDB')
        # create_table(cur)
        # insert_data(cur, account, username, password)
        # fetch_data(cur)

        # Close the connection
        con.close()

def generate_button():
    # Use columns to keep button to the right of the side bar
    col1, col2 = st.sidebar.columns([0.7, 0.4])
    col2.button("Ready to Generate ➡️")