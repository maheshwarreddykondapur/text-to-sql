from database.sql_connect import connect_to_database
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError, SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


def execute_query(query: str) -> None | dict:
    try:
        session = connect_to_database()
    except Exception as e:
        logger.error("Failed to connect to database.", exc_info=e)
        return None, "Failed to connect to database."

    try:
        result = session.execute(text(query))
        data = result.fetchall()  # fetch all rows
        columns = result.keys()

    except SQLAlchemyError as pe:
        logger.error("Invalid SQL Query.", exc_info=pe)
        return None, "Invalid SQL Query."
    except Exception as e:
        logger.error("Query Execution Error.", exc_info=e)
        return None, "Query Execution Error."

    # Closing the session
    session.close()

    if data:
        return columns, data
    else:
        return None, "No results for the query."
