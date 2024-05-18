import streamlit as st
from snowflake.cortex import Complete, ExtractAnswer, Sentiment, Summarize, Translate
import components as cp
import dbConnection as conn
import extra_streamlit_components as stx

Job_type_list = { "SWE" : 'Software Engineer', "MLE" : 'Machine Learning Engineer', "DS": 'Data Scientist', "DA": 'Data Analyst'}

# # Initialize keys in session state
# if "file_history" not in st.session_state:
#     st.session_state["file_history"] = job_file_history_map.copy()

if "db_connection" not in st.session_state:
    st.session_state["db_connection"] = False

if "Job_type_list" not in st.session_state:
    st.session_state["Job_type_list"] = Job_type_list.copy()

if "job_type" not in st.session_state:
    st.session_state["job_type"] = None

if "data" not in st.session_state:
    st.session_state.data = []

# Side bar and main area
col1, col2 = st.columns([1, 3]) 

# Components that go into the left side bar
with col1:
    account, username, password, submit = cp.connection_parameters_input()
    if "username" "password" "account" not in st.session_state:
        st.session_state["username"] = username
        st.session_state["password"] = password
        st.session_state["account"] = account

    # Only when submit is clicked, move on to other view
    if submit:
        new_session, error = conn.connection(account, username, password)
        # Uer entered correct info
        if new_session and not error:
            # Key value set db_connection to true in session state
            st.session_state["db_connection"] = True
            cp.db_connect_success( username, password, account)
        # There is error on db connection
        elif not new_session and error:
            st.session_state["db_connection"] = False
            cp.db_connect_error(error)
    
    if st.session_state["db_connection"] == True:
        st.session_state.job_type= cp.job_type_select(st.session_state.Job_type_list)
        cp.file_upload(st.session_state.job_type)
        cp.job_description_input()
        cp.addtional_info_input()
        # cp.file_history(st.session_state["file_history"], job_type)
        cp.generate_button()

# Components that go into the main area
with col2:
    # cp.title()
    # cp.app_introduction()
    cp.getfile_Content()


# # Check if message key is already in the session state
# if "messages" not in st.session_state:
#     # if not add key to session state and value
#     st.session_state["messages"] = [
#         {
#             "role": "assistant",
#             "content": "how can I help?",
#         }
#     ]

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])


# prompt = st.chat_input("Type your message")

# # if user entered message, append value to current session
# if prompt:
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     with st.chat_message("user"):
#         st.markdown(prompt)
    
#     with st.chat_message("assistant"):  
#         context = ",".join(f"role:{message['role']} content:{message['content']}" for message in st.session_state.messages)
#         print(context)
#         response = Complete(const.SNOWFLAKE_ARCTIC_MODEL, f"Instructions:{const.INSTRUCTIONS}, Context:{context}, Prompt:{prompt}", session = new_session)
#         st.markdown(response)
    
#         st.session_state.messages.append({
#             'role': 'assistant',
#             'content': response
#         })