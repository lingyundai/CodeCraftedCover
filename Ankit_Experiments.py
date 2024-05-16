from snowflake.snowpark import Session
import pandas as pd
from io import StringIO, BytesIO
from PyPDF2 import PdfReader
import streamlit as st
from snowflake.cortex import Complete, ExtractAnswer, Sentiment, Summarize, Translate
from docx import Document

# Create a new session with Snowflake
connection_parameters = {
    "account": "zyb91762.us-east-1",
    "user": "AKUMAR37",
    "password": "Ankitkr@123",
  }  

new_session = Session.builder.configs(connection_parameters).create()
# End of snippet


#---------------------------------------------------------------------#
# Path: Ankit_Experiments.py
# Application to write the cover letter
#---------------------------------------------------------------------#
st.title('Cover letter Generator', anchor=False)
st.sidebar.title('Cover letter Generator')
# Choose a Cortex model
model = st.sidebar.selectbox("Choose a model", 
                     [
                         'mistral-large',
                         'reka-flash',
                         'llama2-70b-chat', 
                         'mixtral-8x7b', 
                         'mistral-7b',
                    ]
)
uploaded_file = st.sidebar.file_uploader("Upload your resume in pdf", type=['pdf','docx'], accept_multiple_files=True)
# for uploaded_file in uploaded_file:
#     st.write("filename:", uploaded_file.name)
# Instructions appended to every chat, and always used 
instructions = "Be concise. Do not hallucinate"

if uploaded_file is not None:
    for file in uploaded_file:
        # To read file as bytes:
        bytes_data = file.read()

        if file.type == 'application/pdf':
            # Handle PDF files
            reader = PdfReader(BytesIO(bytes_data))
            text = []
            for page in reader.pages:
                text.append(page.extract_text())
            st.write(' '.join(text))
        elif file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            # Handle DOCX files
            doc = Document(BytesIO(bytes_data))
            text = []
            for para in doc.paragraphs:
                text.append(para.text)
            st.write(' '.join(text))
        else:
            st.write("Unsupported file type")

# Initialize message history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            'role': 'Alex',
            'content': 'how can I help?'
        }
    ]

# Show the conversation history
st.subheader(f"Conversation with {model}", anchor=False, divider="gray")
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


prompt = st.chat_input("Type your message")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):  
        context = ",".join(f"role:{message['role']} content:{message['content']}" for message in st.session_state.messages)
        response = Complete(model, f"Instructions:{instructions}, Context:{context}, Prompt:{prompt}",session = new_session)
        st.markdown(response)
    
        st.session_state.messages.append({
            'role': 'assistant',
            'content': response
        })