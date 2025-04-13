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
    st.markdown(
        """
        This application is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
        """,
        unsafe_allow_html=True,
    )
    st.header("Insurance Claims Explorer")
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
    selected_function = st.radio(
        "Select your interface.", ["Bot Interface", "Query Executor"]
    )

    # Depending on the selected option, display the corresponding form.
    if selected_function == "Bot Interface":

        st.button("Start New", on_click=clear_messages)

        # Initialize the chat messages history
        if not st.session_state.get("messages", []):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Hi! I can answer your questions related to claims.",
                    "avatar": "🤖",
                }
            ]
        try:
            # Display the prior chat messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                    if message["role"] == "assistant" and message.get(
                        "sql_query", None
                    ):
                        st.code(
                            message.get("sql_query"), language="sql", line_numbers=True
                        )
        except Exception as e:
            logger.error("Error displaying error messages.", exc_info=e)
            st.error("Failed to fetch all the previous messages.", icon="🚨")

        try:
            if prompt := st.chat_input("Your question"):
                st.session_state.messages.append(
                    {
                        "role": "user",
                        "content": prompt,
                    }
                )
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.spinner("Thinking..."):

                    # Generating response for users question
                    response = bot_graph_obj.invoke(
                        {
                            "user_question": st.session_state.messages[-1]["content"],
                            "chat_history": st.session_state.messages[:-1],
                        }
                    )

                    # Print the response as a new message from the assistant
                    chatbot_message_response = st.chat_message("assistant")
                    if response.get("message", None):
                        chatbot_message_response.markdown(response.get("message"))
                    if response.get("sql_query", None):
                        chatbot_message_response.code(
                            response.get("sql_query"), language="sql", line_numbers=True
                        )

                    message = {
                        "role": "assistant",
                        "content": response.get("message"),
                        "sql_query": response.get("sql_query"),
                    }

                    # Add response to message history
                    st.session_state.messages.append(message)

        except Exception as e:
            logger.error("Error generating response to user question.", exc_info=e)
            st.error("Failed to generate response to your question.", icon="🚨")

    elif selected_function == "Query Executor":

        st.write(
            "<b>SQL Query execution interface.</b>",
            unsafe_allow_html=True,
        )

        try:
            if query := st.text_input("Query Editor", placeholder="Type your query."):
                with st.spinner("Your query is running..."):
                    # Generate and add the bot's response.
                    columns, data = execute_query(query)

                    if columns:
                        df = pd.DataFrame(data, columns=columns)
                        st.dataframe(df)  # displays an interactive table
                    else:
                        st.error(data)
        except Exception as e:
            logger.error("Error executing the sql query.", exc_info=e)
            st.error("Failed to execute the SQL query.", icon="🚨")


if __name__ == "__main__":
    main()
