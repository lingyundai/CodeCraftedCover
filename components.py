import streamlit as st
import service as serv
import dbOperation as dbOps
def title():
    st.title("Generate Better Cover Letter", anchor=False)
    st.subheader("That Actually Works.")

def app_introduction():
    st.write("Many cover letter generators take minimal information and generate a terrible cover letter that")
    st.write("1. Obviously is generated with AI - robotic words, inaccurate information.")
    st.write("2. Provide no substantial information that hiring manager wants to see - repetitive content, too generalized.")
    st.write("Result In 'Unfortunately...' e-mails, bad impression, frustration, time wasted for both parties.")
    st.write("This application will fix that!! Hopefully, in these ways -")
    st.write("1. We use comprehensive information to generate a detailed, useful cover letter for the job type you are applying to.")
    st.write("2. We keep history of the files you uploaded, overtime, the cover letter just gets more and more personalized for you and your desired job type.")
    st.write("3. Chat GPT? NO! We use the Snowflake LLM technology 'mistral-large' that generates high-quality models.")
    st.write("In the end, we are in this together. Happy generating!")

def connection_parameters_input():
    account = st.text_input('Enter Snowflake Account', 
                                    placeholder="Your Snowflake account",
                                    help="Please use region that supports 'mistral-large' model. [Need Help?](https://docs.snowflake.com/user-guide/snowflake-cortex/llm-functions?utm_cta=website-homepage-workload-button-explore-platform)")
    username = st.text_input('Enter Snowflake Username', placeholder="Your Snowflake username")
    password = st.text_input('Enter Snowflake Password', placeholder="Your Snowflake password", type='password')
    submit = st.button("Connect")
    return account, username, password, submit


def job_type_select(job_type_list):
    job_type = st.sidebar.selectbox(
        "Select Job Type", 
        job_type_list.values(),
        help="This will help us to create designated chats for you.")
    dbOps.create_table(st.session_state.database_conn_token.cursor(), job_type.replace(' ', '_'))
    if st.session_state.job_type != job_type:
        st.session_state.uploaded_file = None
        st.session_state.upload_key += 1
    serv.show_uploaded_files(st.session_state.database_conn_token.cursor(), job_type.replace(' ', '_'))
    return job_type

def generate_button():
   with st.form("my_form"):
        st.session_state.job_description = st.sidebar.text_area("Enter Job Description", 
                                                                placeholder="Copy-and-paste the job description, the more information the better!",
                                                                value=st.session_state.job_description)
        st.session_state.additional_info = st.sidebar.text_area("Anything Else That Would Help?", 
                    placeholder="For example, 'please do not copy and paste things from job description to the cover letter!' or 'I am also experienced in xxx'.",
                    value=st.session_state.additional_info)
        submit = st.sidebar.button("Submit")
        if submit:
            if st.session_state.job_description and st.session_state.additional_info and st.session_state.fetched_data:
                st.session_state.isGenerated = True
                st.sidebar.caption("Successfully Submitted!")
            else:
                st.session_state.isGenerated = False
                st.sidebar.caption("Please check if you have atleast uploaded a files, entered job description and additional information.")

def file_not_found_error():
    st.warning("Session state file not found. Starting with an empty session state.")

def json_decode_error():
    st.error("Error decoding session state file. Starting with an empty session state.")

def connection_establish():
    st.caption("Successfully Connected!")

def credential_not_valid():
    st.caption("Please enter valid credentials")

def render_ui():
    st.rerun()

def theme():
    if st.session_state.theme_button:
        # dark theme
        st._config.set_option('theme.backgroundColor', '#1f1f1f')
        st._config.set_option('theme.primaryColor', '#4a89eb')
        st._config.set_option('theme.secondaryBackgroundColor', '#6b6b6b')
        st._config.set_option('theme.textColor', '#ffffff')
    else:
        # light theme
        st._config.set_option('theme.backgroundColor', '#FFFFFF')
        st._config.set_option('theme.primaryColor', '#4a89eb')
        st._config.set_option('theme.secondaryBackgroundColor', '#F0F2F6')
        st._config.set_option('theme.textColor', '#262730')

def update_theme():
    st.session_state.theme_button = not st.session_state.theme_button
    theme()

def theme_toggle():
    st.toggle(label='🌞 🌚', value=st.session_state.theme_button, on_change=update_theme)