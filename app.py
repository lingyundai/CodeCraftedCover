import streamlit as st
import components as cmpnt
import dbConnection as conn
import service as serv
import cover_letter_generator as clg
# Load session state from JSON file
serv.load_session_state_from_json()

# Main Container sign in and sign out status
if st.session_state.db_connection == False:
    cmpnt.title()
    cmpnt.app_introduction()
    st.write("Please use your snowflake account to sign in.")
    if st.button("Sign In"):
        serv.user_sign_in()

# Side bar and main area after user signed in
col1, col2 = st.columns([3, 12])

# Components that go into the left side bar
with col1:    
    if st.session_state.db_connection == True:
        st.session_state.job_type= cmpnt.job_type_select(st.session_state.Job_type_list)
        serv.file_upload(st.session_state.job_type)
        cmpnt.generate_button()

# Components that go into the main area
with col2:
    if st.session_state.db_connection == True:
        serv.user_signed_in()
        serv.getfile_Content()
if st.session_state.isGenerated == True:
    clg.chatbot()
