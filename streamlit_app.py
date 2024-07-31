
import sys
import time 
import streamlit as st

from streamlit_chat import message
from source.LLMUcamp import LLMUcamp

def typed_answer(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.05)

def launch_app(chatbot: LLMUcamp, user_icon, chatbot_icon):
    st.title("🎓 Chatbot Vestibular Unicamp 2025 - LLMUcamp")
    st.markdown(
    """
        <style>
            .st-emotion-cache-janbn0 {
                flex-direction: row-reverse;
                text-align: right;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )
    
    avatar_dict = {"user": user_icon, "assistant": chatbot_icon}

    # Initialize the chat messages history
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{
            "role": "assistant", 
            "content": "Olá! Estou aqui para ajudar com suas dúvidas sobre o VU 2025. Qual é sua pergunta ?"
        }]

    # Prompt for user input and save
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})

    # Display the existing chat messages
    for message_data in st.session_state.messages:
        role    = message_data["role"]
        content = message_data["content"]   
        with st.chat_message(role, avatar=avatar_dict[role]):
            st.markdown(f"{content}")
    
    # If last message is not from assistant, we need to generate a new answer
    if st.session_state.messages[-1]["role"] != "assistant": 
        # Call the chatbot function
        with st.chat_message("assistant", avatar=avatar_dict["assistant"]):
            with st.spinner("Pensando..."):
                answer = chatbot.answer(prompt)  # Call the chatbot function with the user's prompt
                st.write_stream(typed_answer(answer))

        message = {"role": "assistant", "content": answer}
        st.session_state.messages.append(message)

if __name__ == "__main__":
    vectorstore_folder = sys.argv[1]
    user_icon          = sys.argv[2]
    chatbot_icon       = sys.argv[3]
    model              = sys.argv[4]
    
    chatbot = LLMUcamp(vectorstore_folder=vectorstore_folder, temperature=0, model=model) 
    launch_app(chatbot, user_icon, chatbot_icon) 
