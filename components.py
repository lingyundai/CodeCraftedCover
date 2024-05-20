import streamlit as st
import snowflake.cortex as cortex 
import dbConnection as dbConn
import dbOperation as dbOps 
import pandas as pd
from io import StringIO, BytesIO
from PyPDF2 import PdfReader
from docx import Document
import cover_letter_generator as clg



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
    
    con = dbConn.databaseConnection(st.session_state.username, st.session_state.password , st.session_state.account)
    cur = con.cursor()
    dbOps.switch_database(cur, 'USERDB')
    table_name = job_type.replace(' ', '_')
    dbOps.create_table(cur, table_name)
    for data in text:
        dbOps.insert_data(cur, table_name, data)
    show_uploaded_files(cur, table_name)

def show_uploaded_files(cur, table_name):
    # Fetch all data from the table
    st.session_state.data = dbOps.fetch_data(cur, table_name)
    # print(st.session_state.data)
    # Display the filenames
    filenames = [row[0] for row in st.session_state.data]
    # print(filenames)
    st.sidebar.write("Click on the file name to delete it.")
    for i, filename in enumerate(filenames):
        if st.sidebar.button(filename , key=f"delete_{filename}"+ f" ({i+1})"):
            dbOps.delete_file(cur, table_name, filename)
            # re-render
            st.rerun()

def job_description_input():
    st.sidebar.text_area("Enter Job Description", 
                         placeholder="Copy-and-paste the job description, the more information the better!")
    if st.sidebar.button("Submit"):
        st.sidebar.caption("Successfully Submitted!")

def addtional_info_input():
    st.sidebar.text_area("Anything Else That Would Help?", 
                 placeholder="For example, 'please do not copy and paste things from job description to the cover letter!' or 'I am also experienced in xxx'.")

def submit_button():
    st.button("Generate")

def connection_parameters_input():
    account = st.text_input('Enter Snowflake Account', 
                                    placeholder="Your Snowflake account",
                                    help="One of the Snowflake commercial regions, besides us-east as our LLM is not currently avaliable in those regions." ,value = st.secrets["account"])
    username = st.text_input('Enter Snowflake Username', placeholder="Your Snowflake username" ,value = st.secrets["username"])
    password = st.text_input('Enter Snowflake Password', placeholder="Your Snowflake password", type='password', value = st.secrets["password"])
    submit = st.button("Connect")
    return account, username, password, submit


def job_type_select(job_type_list):
    job_type = st.sidebar.selectbox(
        "Select Job Type", 
        job_type_list.values(),
        help="This will help us to create designated chats for you.")
    return job_type

def generate_button():
   with st.form("my_form"):
        st.session_state.job_description = st.sidebar.text_area("Enter Job Description", placeholder="Copy-and-paste the job description, the more information the better!")
        st.session_state.addition_info = st.sidebar.text_area("Anything Else That Would Help?", 
                    placeholder="For example, 'please do not copy and paste things from job description to the cover letter!' or 'I am also experienced in xxx'.")
        submit = st.sidebar.button("Submit")
        if submit:
            if st.session_state.job_description and st.session_state.addition_info and st.session_state.fetched_data:
                st.sidebar.caption("Successfully Submitted!")
            else:
                st.sidebar.caption("Please check if you have atleast uploaded a files, entered job description and additional information.")


def chatbot():
    instructions = "Be concise. Do not hallucinate"

    # Initialize message history in session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                'role': 'assistant',
                'content': "Hello! I'm here to help you generate a cover letter. Please upload files and provide job description to get started."
                # 'content': st.session_state.fetched_data if len(st.session_state.fetched_data) > 0 else "No files uploaded yet. Please upload files to generate cover letter."
            }
        ]
    # User input prompt
    prompt = st.chat_input("Type your message", key="chat_input")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.isFirstPrompt = True

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):  
            context = ",".join(f"role:{message['role']} content:{message['content']}" for message in st.session_state.messages)
            response = cortex.Complete('mistral-large', f"Instructions:{instructions}, context:{context}, Prompt:{prompt}",session = st.session_state.new_session)
            st.markdown(response)

            st.session_state.messages.append({
                'role': 'assistant',
                'content': response
            })


        # Scroll to the last message
        st.write('<meta name="viewport" content="width=device-width, initial-scale=1">', unsafe_allow_html=True)
        st.write('<script>var element = document.body; element.scrollTop = element.scrollHeight;</script>', unsafe_allow_html=True)

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
    # Use columns to keep button to the right of the side bar
    col1, col2 = st.sidebar.columns([0.7, 0.4])
    col2.button("Ready to Generate ➡️")


def getfile_Content():
    job_description_input="About the job: Company Description: Who We Are: Interested in joining our team? Here is some more information about us! Momentus provides industry-leading event and venue management software to customers in over 50 countries around the world, serving thousands of customers that power millions of events. In the age of digital transformation, our comprehensive platform offers event professionals leading-edge SaaS technology that provides a 360 view of their business, allowing them to cut costs, save time, and increase revenue. Momentus is used for top shows from across the world, famous museums, global convention centers, performing arts venues, professional sports arenas, and other unique events. Our client list includes The Apollo Theatre, Mercedes-Benz Stadium, Harvard University, Portland'5 Centers for the Arts, the Javitz Center, and St. Louis Art Museum. Some of our global clients include: ExCel London, Museum of Contemporary Art Australia, the Porsche Experience Center in Germany and the Sydney Opera House. Working @ Momentus: Surround yourself with highly motivated co-workers that push you to be your best each day. Momentus offers the career opportunities and fast-paced, exciting environment of a growth company where you can make a direct impact on our product and customers. Job Description: As a Software Engineering Intern, you will have the opportunity to participate in various stages of software development, from design to implementation. You will work alongside experienced engineers to contribute to engineering efforts aimed at solving complex problems. This role requires strong technical skills, a collaborative mindset, and a passion for innovation. Location: Remote Duration: End of May-August 2024. Participate in formal design and implementation activities. Write effective, maintainable and well-tested code. Contribute to engineering efforts to solve complex engineering problems. Design and develop front-end services in javascript/typescript using Vue. Work with engineering teams to debug solutions & features. Effectively collaborate with technical leaders in a multi-team environment. Demonstrate flexibility and resilience in the face of changing priorities and requirements. Write effective, maintainable and well-tested code. Contribute to engineering efforts to solve complex engineering problems. Qualifications: Currently enrolled in a bachelor’s degree program majoring in Computer Science. Proficient in Javascript/Typescript. Basic Experience in working with either React, Vue, or Angular. A strong desire to innovate industry leading software. Demonstrated skill in time management and completing projects in a collaborative team environment. Previous internship experience working in a technical or engineering environment. Good written and verbal communication, including presentation skills. Familiarity with Git. Additional Information: No Dress Code: We value your individuality. Come as you are - because we know you're smart enough to choose what to wear. Teammate Recognition Rewards and Swag: Celebrate milestones and enjoy the largest reward network ever in partnership with Awardco. Flexible Career: We believe in work that works for you. Get the job done where and when you work best. It's about winning at life by loving your job. Professional Development: Unlock unlimited training opportunities through LinkedIn Learning to sharpen your skills and advance your career. Love Your Job, Win at Life: When you love what you do, every day feels like a victory. Join us and embrace a career that's worth celebrating. At Momentus, we cultivate a culture of inclusion for all employees that respects their individual strengths, views, and experiences. We believe that our differences enable us to be a better team – one that makes better decisions, drives innovation and delivers better business results. Momentus is an equal opportunity employer and does not discriminate based on race, religion, national origin, age, sex, gender identity, disability, sexual orientation, marital status, or any other basis protected by law"
    # st.write(st.session_state.data)
    if len(st.session_state.data) > 0:
        clg.generate_cover_letter(st.session_state.data[0][1]+st.session_state.data[1][1], job_description_input)
        # for row in st.session_state.data:
        #     st.write(row[1])
    else:
        st.write("")