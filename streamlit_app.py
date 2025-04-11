from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import pandas as pd
import logging
import os
import streamlit as st

# Load environment  variables
load_dotenv(dotenv_path=".env", override=True)

from database.helper import execute_query
from utils.execution_graph import bot_compiled_graph





# Set up basic configuration for logging
logging.basicConfig(
    level=logging.INFO,  # Log messages at this level or higher
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",  # Custom log message format
    datefmt="%Y-%m-%d %H:%M:%S",  # Date format
)

logger = logging.getLogger("streamlit_app")
bot_graph_obj = bot_compiled_graph()

def clear_messages():
    st.session_state.messages = []

def main():
    st.title("Insurance Claims Explorer")
    st.session_state.user_avatar = "👾"
   

    # Inject custom CSS to display radio options side by side.
    st.markdown(
        """
        <style>
        /* Change the radio group's layout to horizontal */
        div[role="radiogroup"] {
            display: flex;
            flex-direction: row;
        }
        div[role="radiogroup"] label {
            margin-right: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Toggle between the two function modes using a radio button.
    selected_function = st.radio("Select your interface.", ["Bot Interface", "Query Executor"])

    # Depending on the selected option, display the corresponding form.
    if selected_function == "Bot Interface":
            
        # Initialize the chat messages history
        if not st.session_state.get("messages", []): 
            st.session_state.messages = [
                {"role": "assistant", "content": "Hi! I can answer your questions related to claims.", "avatar": "🤖"}
            ]
        
        if prompt := st.chat_input("Your question"): 
            st.session_state.messages.append({"role": "user", "content": prompt, "avatar": st.session_state.user_avatar})
        st.button("Start New", on_click= clear_messages)
        # Display the prior chat messages
        for message in st.session_state.messages: 
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message.get("sql_query", None):
                    st.code(message.get("sql_query"), language="sql", line_numbers=True)

        # If last message is not from assistant, generate a new response
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.spinner("Thinking..."):
                response = bot_graph_obj.invoke({
                "user_question": st.session_state.messages[-1]["content"],
                "chat_history": st.session_state.messages[:-1]
            })
            
                # update the last message
                st.session_state.last_message = response
            logger.info(response)
            # Print the response as a new message from the assistant
            chatbot_message_response = st.chat_message("assistant", avatar="🤖")
            if response.get("message", None):
                chatbot_message_response.markdown(response.get("message"))
            if response.get("sql_query", None):
                chatbot_message_response.code(response.get("sql_query"), language="sql", line_numbers=True)
            
            message =  {"role": "assistant", "content": response.get("message"), "sql_query": response.get("sql_query")}

            # Add response to message history
            st.session_state.messages.append(message)
        
    elif selected_function == "Query Executor":

        st.write(
            "<b>SQL Query execution interface.</b>",
            unsafe_allow_html=True,
        )
        
        if query := st.text_input("Query Editor", placeholder="Type your query."):
            with st.spinner("Your query is running..."):
                # Generate and add the bot's response.
                columns, data = execute_query(query)

                if columns:
                    df = pd.DataFrame(data, columns=columns)
                    st.dataframe(df)  # displays an interactive table
                else:
                    st.error(data)


if __name__ == "__main__":
    main()
