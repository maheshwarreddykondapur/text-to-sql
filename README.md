# Text-to-SQL Chatbot

A powerful, yet simple chatbot that transforms natural language questions about insurance claims into SQL queries. With the integration of the GPT-4o model, this application not only generates the queries but also executes them, returning clear text responses based on your database's information. This project is designed to help both technical and non-technical users seamlessly query complex claim data.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Overview

Text-to-SQL leverages natural language processing with GPT-4 to understand user queries related to insurance claims and automatically convert them into SQL queries. Once a query is generated, it is executed against a backend database, and the results are relayed back to the user in an understandable text format. This innovative approach simplifies data exploration and decision-making, removing the need for deep technical knowledge in SQL.

---

## Features

- **Natural Language Querying:** Users can ask questions in plain language about insurance claims.
- **Automated SQL Generation:** The system converts natural language into SQL queries based on the extracted context.
- **Database Interaction:** Executes dynamically created SQL queries to fetch data from the insurance claims database.
- **GPT-4o Powered Responses:** Uses the GPT-4o model to process queries and generate human-like responses.
- **User-Friendly Interface:** Built with Streamlit, offering a clean and interactive dashboard.

---

## Prerequisites

Before setting up or running the project, ensure you have the following installed:

- **Python 3.11+**  
- **Streamlit** (for the web application interface)
- Familiarity with virtual environments (using `venv` or similar)
- Basic understanding of SQL and environment variable configuration

---

## Installation & Setup

Follow these steps to get your Text-to-SQL Chatbot running locally:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/text-to-sql.git
   cd text-to-sql

2. **Create a Python Virtual Environment:**

    ```bash
    python -m venv .venv
    
3. **Activate the Virtual Environment:**

    **On Windows:**

    ```bash
    .venv\Scripts\activate
    ```
    
    **On macOS/Linux:**
    
    ```bash
    source .venv/bin/activate

4. **Install the Required Packages:**

    Install dependencies from the requirements.txt file:

    ```bash
    pip install -r requirements.txt

5. **Set Up the Database:**

    Before setting up the database, modify the input file name in database_setup.py as needed. Then run:

    ```bash
    python database_setup.py
    Configure Environment Variables:

6. **Create a .env file from the provided example file:**

    ```bash
    cp .env-example .env
    
7. **Launch the Streamlit Application:**

    Start the Chatbot using Streamlit

    ```bash
    streamlit run streamlit_app.py

---

## How It Works

1. **User Query Input:**  
   The chatbot receives a natural language question about insurance claims from the user.

2. **Natural Language Processing:**  
   GPT-4o processes the query to extract relevant details and context.

3. **SQL Query Generation:**  
   Based on the extracted information, the application formulates a suitable SQL query to fetch relevant data.

4. **Query Execution:**  
   The SQL query is executed against the database, and the results are retrieved.

5. **Response Formation:**  
   The retrieved data is converted into a clear, human-readable text format using GPT-4o and displayed to the user.

This end-to-end workflow simplifies data querying and analysis for both technical and non-technical users.

---

## Further Exploration

- Handle multiple questions in a single turn.
- Creating detailed error handling and logging for SQL execution.
- Adding detailed definitons to colums in the database schema.
- Extensive testing and Bugfixes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.


