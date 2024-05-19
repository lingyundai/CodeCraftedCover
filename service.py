import json
import streamlit as st
import snowflake.connector as sfconn
from io import StringIO, BytesIO
from PyPDF2 import PdfReader
from docx import Document
import dbConnection as dbConn
import dbOperation as dbOps
import components as cmpnt


# Function to save session state to a file
def load_session_state_from_json(file_path="state.json"):
    try:
        with open(file_path, 'r') as f:
            session_data = json.load(f)
        for key, value in session_data.items():
            if key not in st.session_state:
                st.session_state[key] = value
    except FileNotFoundError:
        cmpnt.file_not_found_eror()
    except json.JSONDecodeError:
        cmpnt.json_decode_error()

def Database_connect(username, password, account):
    if (username and password and account):
        # Connect to the database and store the connection object in the session state
        st.session_state.database_conn_token = dbConn.databaseConnection(username, password, account)
        # Create a cursor object
        cur = st.session_state.database_conn_token.cursor()
        # Create a new database
        dbOps.create_database(cur, 'userDB')
        # Switch to the new database
        dbOps.switch_database(cur, 'userDB')
        # Close the connection
        # st.session_state.database_conn_token.close()
        cmpnt.connection_establish()
        st.session_state.db_connection = True

    else:
        cmpnt.credential_not_valid()
        st.session_state.db_connection = False

def file_upload(job_type):
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
        cur = st.session_state.database_conn_token.cursor()
        table_name = job_type.replace(' ', '_')
        dbOps.create_table(cur, table_name)
        for data in text:
            dbOps.insert_data(cur, table_name, data)
        show_uploaded_files(cur, table_name)


def show_uploaded_files(cur, table_name):
    # Fetch all data from the table
    st.session_state.data = dbOps.fetch_data(cur, table_name)
    # Display the filenames
    filenames = [row[0] for row in st.session_state.data]
    # print(filenames)
    if len(filenames) > 0:
        st.sidebar.write("Click on the file name to delete it.")
        for i, filename in enumerate(filenames):
            if st.sidebar.button(filename):
                dbOps.delete_file(cur, table_name, filename)
                # re-render
                st.rerun()

def getfile_Content():
    # st.write(st.session_state.data)
    if len(st.session_state.data) > 0:
        for row in st.session_state.data:
            st.session_state.fetched_data.append(row[1])
    else:
        st.session_state.fetched_data = []


@st.experimental_dialog("User Sign In")
def user_sign_in():
    account, username, password, submit = cmpnt.connection_parameters_input()
    if "username" "password" "account" not in st.session_state:
        st.session_state.username = username
        st.session_state.password = password
        st.session_state.account = account

    # Only when submit is clicked, move on to other view
    if submit:
        st.session_state_new_session, error = dbConn.connection(account, username, password)
        # Uer entered correct info
        if st.session_state_new_session and not error:
            # Key value set db_connection to true in session state 
            Database_connect(username, password, account)
            st.session_state.db_connection = True
            st.rerun()