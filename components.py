import streamlit as st

# main page component
# title of the application
def title():
    st.title("Generate 'The Right' Cover Letter")

def file_upload():
    st.file_uploader("Upload Resume", type="pdf")

def job_description_input():
    st.text_area("Enter Job Description", placeholder="Copy-and-paste the job description")

def addtional_info_input():
    st.text_area("How Do You Like Your Cover Letter Generated?", 
                 placeholder="What should we avoid? Such as 'please do not copy and paste things from job description to the cover letter!'")

def submit_button():
    st.button("Generate")

# side bar components
def api_key_input():
    st.sidebar.text_input('Enter Your API Key', 
                                placeholder="Enter your API key", type='password')

