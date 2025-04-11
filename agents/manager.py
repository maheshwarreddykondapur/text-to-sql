from typing import Any
from agents.sql import sql_agent_pipeline
from agents.query_transformation import transform_query_agent_pipeline
from agents.response_generation import response_generation_agent_pipeline


class agent_manager:
    """
    Manager of all the required pipelines by the orchestrator.
    """

    def __init__(self) -> None:
        self.list_of_agents: dict = {}
        self.list_of_agents["sql_agent"] = sql_agent_pipeline()
        self.list_of_agents["response_generator"] = response_generation_agent_pipeline()
        self.list_of_agents["transform_question"] = transform_query_agent_pipeline()

    def get_llm_agent(self, agent_name) -> NotImplementedError | Any:
        if agent_name not in self.list_of_agents:
            return NotImplementedError("This agent is not implemented yet. ")

        return self.list_of_agents[agent_name]
