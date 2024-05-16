import streamlit as st
from snowflake.cortex import Complete, ExtractAnswer, Sentiment, Summarize, Translate
import components as cp
import constants as const
import dbConnection as conn


job_file_history_map = {
    const.SOFTWARE_ENGINEER: [],
    const.MACHINE_LEARNING_ENGINEER: [],
    const.DATA_SCIENTIST: ["temp_ds_xxxx.pdf", "temp1_ds_xxxxxxxxx.docx"],
    const.DATA_ANALYST: [],
    const.DATA_ENGINEER: [],
    const.PRODUCT_MANAGER: [],
    const.PROJECT_MANAGER: ["temp_Proj_new.pdf"],
    const.TEST_ENGINEER: [],
}

if "file_history" not in st.session_state:
    st.session_state["file_history"] = job_file_history_map.copy()

# Side bar and main area
col1, col2 = st.columns([1, 3]) 

# Components that go into the left side bar
with col1:
    account, username, password = cp.connection_parameters_input()
    new_session, error = conn.connection(account, username, password)
    # Uer entered correct info
    if new_session and not error:
        cp.db_connect_success()
        job_type = cp.job_type_select(st.session_state["file_history"])
        cp.file_upload()
        cp.job_description_input()
        cp.addtional_info_input()
        cp.file_history(st.session_state["file_history"], job_type)
        cp.generate_button()
    # There is error on db connection
    elif not new_session and error:
        cp.db_connect_error(error)

# Components that go into the main area
with col2:
    cp.title()
    cp.app_introduction()


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