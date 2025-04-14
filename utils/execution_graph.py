from langgraph.graph import StateGraph, END, START
from typing import Any, TypedDict
from langgraph.graph.state import CompiledStateGraph
import logging
import pandas as pd

from agents import agent_manager
from database.helper import execute_query
from utils.common import generate_plotly_chart

agent_runner = agent_manager()
logger = logging.getLogger(__name__)


class conversation_flow_states(TypedDict):
    user_question: str
    transformed_question: str
    sql_query: str
    chat_history: str
    message: str
    process_successful: bool
    is_relevant_question: bool
    chart: Any


def transform_question(state) -> dict[str, str]:
    """
    Responsible for transforming user question by adding more context to it.
    """
    try:

        initial_transform = agent_runner.get_llm_agent(agent_name="transform_question")

        result_query = initial_transform.execute_agent(
            user_query=state["user_question"], chat_history=state["chat_history"]
        ).__dict__

        logger.info(result_query)

        if result_query["is_not_related"]:

            return {
                "message": result_query["message"],
                "process_successful": True,
                "is_relevant_question": False,
                "user_question": state["user_question"],
                "transformed_question": None,
            }
        else:

            return {
                "process_successful": True,
                "transformed_question": result_query["transformed_question"],
                "message": None,
                "is_relevant_question": True,
                "user_question": state["user_question"],
            }

    except Exception as e:

        logger.error("Failed to transform a question.", exc_info=e)

        return {
            "process_successful": True,
            "transformed_question": state["user_question"],
            "message": None,
            "is_relevant_question": True,
            "user_question": state["user_question"],
        }


def sql_generator(state) -> dict[str, str]:
    """
    Responsible for generating sql query and validating it.
    """

    try:

        if state["is_relevant_question"]:
            transformed_question = state.get("transformed_question", {})

            question_to_bot = transformed_question or state.get("user_question")

            sql_query_llm_pipe = agent_runner.get_llm_agent(agent_name="sql_agent")

            sql_llm_response = sql_query_llm_pipe.execute_agent(
                user_query=question_to_bot
            ).__dict__
            logger.info(sql_llm_response)
            if sql_llm_response["is_not_related"]:
                return {
                    "is_relevant_question": False,
                    "sql_query": None,
                    "process_successful": True,
                    "message": sql_llm_response["message"],
                }
            else:
                validator_result = sql_query_llm_pipe.execute_validation_agent(
                    **{
                        "sql_query": sql_llm_response["sql_query"],
                        "user_query": question_to_bot,
                    }
                ).__dict__

                if validator_result["valid_query"]:
                    return {
                        "is_relevant_question": True,
                        "sql_query": sql_llm_response["sql_query"],
                        "process_successful": True,
                        "user_question": state["user_question"],
                    }
                else:
                    return {
                        "is_relevant_question": True,
                        "sql_query": validator_result["sql_query"],
                        "process_successful": True,
                        "user_question": state["user_question"],
                    }
        else:
            return {
                "process_successful": True,
                "message": state["message"],
                "is_relevant_question": False,
            }

    except Exception as e:

        logger.error("Failed to generate SQL query.", exc_info=e)

        return {
            "is_relevant_question": False,
            "sql_query": None,
            "message": "Unable to serve the request at the moment.",
            "process_successful": False,
        }


def bot_response_generator(state) -> dict[str, str]:
    """
    Responsible for  generating bot response based on data from the database.
    """

    try:
        if state["is_relevant_question"] and state["process_successful"]:

            columns, rows = execute_query(query=state["sql_query"])

            if not columns:
                return {
                    "sql_query": state["sql_query"],
                    "message": "No data found in the database",
                }

            df = pd.DataFrame(rows, columns=columns)

            response_generation_pipe = agent_runner.get_llm_agent(
                agent_name="response_generator"
            )
            response_result = response_generation_pipe.execute_agent(
                sql_output=df.to_markdown(index=False),
                user_question=state["user_question"],
            ).__dict__

            # Generating plotly chart for the data
            if response_result.get("visualization_info", None):
                chart = generate_plotly_chart(
                    response_result.get("visualization_info"), data_frame=df
                )
            else:
                chart = None

            logger.info(response_result)

            return {
                "message": response_result["response_text"],
                "sql_query": state["sql_query"],
                "chart": chart,
            }

        else:
            return {"message": state["message"], "sql_query": None, "chart": None}
    except Exception as e:

        logger.error("Failed to generate the final response", exc_info=e)

        return {
            "sql_query": state["sql_query"],
            "message": "Failed to execute the query at the moment.",
        }


def bot_compiled_graph():
    pipeline_graph = StateGraph(conversation_flow_states)
    pipeline_graph.add_node("transform_question_node", transform_question)
    pipeline_graph.add_node("sql_generator_node", sql_generator)
    pipeline_graph.add_node("response_generator_node", bot_response_generator)
    pipeline_graph.add_edge(START, "transform_question_node")
    pipeline_graph.add_edge("transform_question_node", "sql_generator_node")
    pipeline_graph.add_edge("sql_generator_node", "response_generator_node")
    pipeline_graph.add_edge("response_generator_node", END)

    compile_graph: CompiledStateGraph = pipeline_graph.compile()

    return compile_graph
