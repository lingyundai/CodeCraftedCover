import streamlit as st
import components as cmpnt
import constants as const
import dbConnection as conn
import service as serv

# Load session state from JSON file
serv.load_session_state_from_json()

# Side bar and main area
col1, col2 = st.columns([3, 11]) 

# Components that go into the left side bar
with col1:
    account, username, password, submit = cmpnt.connection_parameters_input()
    if "username" "password" "account" not in st.session_state:
        st.session_state.username = username
        st.session_state.password = password
        st.session_state.account = account

    # Only when submit is clicked, move on to other view
    if submit:
        st.session_state.new_session, error = conn.connection(account, username, password)
        # Uer entered correct info
        if st.session_state.new_session and not error:
            # Key value set db_connection to true in session state 
            serv.Database_connect( username, password, account)
    
    if st.session_state.db_connection == True:
        st.session_state.job_type= cmpnt.job_type_select(st.session_state.Job_type_list)
        serv.file_upload(st.session_state.job_type)
        cmpnt.generate_button()

# Components that go into the main area
with col2:
    if not st.session_state.isFirstPrompt:
        cmpnt.title()
        cmpnt.app_introduction()
if st.session_state.db_connection == True:
    serv.getfile_Content()
    cmpnt.chatbot()