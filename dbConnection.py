from snowflake.snowpark import Session

def connection(account, username, password):
    # intialize new session and error
    new_session = None
    error = None
    connection_parameters = {
        "account": account,
        "user": username,
        "password": password,
    }  
    try:
        if account and username and password:
            new_session = Session.builder.configs(connection_parameters).create()
            print("New session created successfully!")
            print(new_session)
    except Exception as e:
        error = str(e)
    
    return new_session, error

# def connection_parameters_input():
#     print("sessoion_state",st.session_state)
#     if "connected" not in st.session_state:
#         st.session_state["connected"] = False
 
#     if not st.session_state["connected"]:
#         with st.sidebar.form("connection_parameters"):
#             account = st.text_input('Enter Snowflake Account',
#                                     placeholder="Your Snowflake account",
#                                     help="One of the Snowflake commercial regions, besides us-east as our LLM is not currently avaliable in those regions.")
#             username = st.text_input('Enter Snowflake Username', placeholder="Your Snowflake username")
#             password = st.text_input('Enter Snowflake Password', placeholder="Your Snowflake password", type='password')
#             submit = st.form_submit_button("Connect")
#             if submit:
#                 st.session_state["connected"] = True
#                 return account, username, password
#     else:
#         with st.sidebar.form("logout"):
#             if st.button('Logout'):
#                 st.session_state["connected"] = False