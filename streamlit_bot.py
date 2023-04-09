
import os
import random
import time
import streamlit as st
from datetime import datetime
from streamlit_chat import message
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader


st.markdown("<h1 style='text-align: center; color: red;'>Doc-Bot👋</h1>", unsafe_allow_html=True)

buff, col, buff2 = st.columns([1,3,1])
openai_key = col.text_input('OpenAI Key:')
os.environ["OPENAI_API_KEY"] = openai_key


if 'all_messages' not in st.session_state:
    st.session_state.all_messages = []

def save_uploaded_file(uploadedfile):
  with open(os.path.join("data",uploadedfile.name),"wb") as f:
     f.write(uploadedfile.getbuffer())

# Create a function to get bot response
def get_bot_response(user_query):
    response = index.query(user_query)
    return str(response)

# Create a function to display messages
def display_messages(all_messages):
    for msg in all_messages:
        if msg['user'] == 'user':
            message(f"You ({msg['time']}): {msg['text']}", is_user=True, key=int(time.time_ns()))
        else:
            message(f"Bot ({msg['time']}): {msg['text']}", key=int(time.time_ns()))

# Create a function to send messages
def send_message(user_query, all_messages):
    if user_query:
        all_messages.append({'user': 'user', 'time': datetime.now().strftime("%H:%M"), 'text': user_query})
        bot_response = get_bot_response(user_query)
        all_messages.append({'user': 'bot', 'time': datetime.now().strftime("%H:%M"), 'text': bot_response})

        st.session_state.all_messages = all_messages
        
    
# Create a list to store messages


datafile = st.file_uploader("Upload your doc",type=['docx', 'doc', 'pdf'])
if datafile is not None:
    if not os.path.exists('./data'):
        os.mkdir('./data')
    save_uploaded_file(datafile)
    documents = SimpleDirectoryReader('data').load_data()
    index = GPTSimpleVectorIndex.from_documents(documents)

    index.save_to_disk('index.json')

    index = GPTSimpleVectorIndex.load_from_disk('index.json')

    # Create input text box for user to send messages
    user_query = st.text_input("You: ","", key= "input")

    # Create a button to send messages
    send_button = st.button("Send")

    # Send message when button is clicked
    if send_button:
        send_message(user_query, st.session_state.all_messages)
        display_messages(st.session_state.all_messages)

    

    

    
       

































       