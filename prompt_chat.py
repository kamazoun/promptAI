from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

import streamlit as st
from streamlit_chat import message

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

st.title('Chat with an AI Bot 🤖')

chat = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.5)

# creating the messages (chat history) in the Streamlit session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# creating the sidebar
with st.sidebar:
    # streamlit text input widget for the system message (role)
    system_message = st.text_input(label='System role')

    if system_message:
        if not any(isinstance(x, SystemMessage) for x in st.session_state.messages):
            st.session_state.messages.append(
                SystemMessage(content=system_message)
            )
        elif isinstance(st.session_state.messages[0], SystemMessage):
            st.session_state.messages.clear()
            st.session_state.messages.insert(0, SystemMessage(content=system_message))

user_prompt = st.chat_input("Say something")

# if the user entered a question
if user_prompt:
    st.session_state.messages.append(
        HumanMessage(content=user_prompt)
    )

    with st.spinner('Working on your request ...'):
        # creating the ChatGPT response
        response = chat(st.session_state.messages)

    # adding the response's content to the session state
    st.session_state.messages.append(AIMessage(content=response.content))

if len(st.session_state.messages) >= 1:
    if not isinstance(st.session_state.messages[0], SystemMessage):
        st.session_state.messages.insert(0, SystemMessage(content='You are a helpful assistant.'))

# displaying the messages (chat history)
for i, msg in enumerate(st.session_state.messages[1:]):
    if i % 2 == 0:
        message(msg.content, is_user=True, key=f'{i} + 🤓')  # user's question
    else:
        message(msg.content, is_user=False, key=f'{i} +  🤖')  # ChatGPT response
