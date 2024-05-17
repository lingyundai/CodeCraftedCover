import streamlit as st

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


def file_upload():
    st.sidebar.file_uploader("Upload Files", 
                             type=["pdf", "docx"], 
                             help="Any file that you think would help us to generate a accurate cover letter for you",
                             accept_multiple_files=True)

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
                                    help="One of the Snowflake commercial regions, besides us-east as our LLM is not currently avaliable in those regions.")
    username = st.sidebar.text_input('Enter Snowflake Username', placeholder="Your Snowflake username")
    password = st.sidebar.text_input('Enter Snowflake Password', placeholder="Your Snowflake password", type='password')
    submit = st.sidebar.button("Connect")
    return account, username, password, submit

def job_type_select(session_state):
    job_type = st.sidebar.selectbox(
        "Select Job Type", 
        list(session_state.keys()),
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

def db_connect_success():
    st.sidebar.caption("Successfully Connected!")

def generate_button():
    # Use columns to keep button to the right of the side bar
    col1, col2 = st.sidebar.columns([0.7, 0.4])
    col2.button("Ready to Generate ➡️")