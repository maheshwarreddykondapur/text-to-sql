from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os

from prompts import transform_query_prompt
from response_structures import transform_question_structure


class transform_query_agent_pipeline:
    def __init__(self) -> None:

        self.llm_model = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL"), api_key=os.getenv("OPENAI_KEY")
        )

        self.transform_query_pipeline = self._setup_transform_query_pipeline()

    def execute_agent(self, **kwargs) -> None:
        """
        Executes the question transformation pipeline.

        Args:
            user_query (str): The query provided by the user.

        """

        user_query = kwargs.get("user_query", "")
        chat_history = kwargs.get("chat_history", "")
        return self.transform_query_pipeline.invoke(
            {"user_query": user_query, "chat_history": chat_history}
        )

    def _setup_transform_query_pipeline(
        self,
    ): 
        """Sets up the question transformation chain using modular components."""
        try:
            return PromptTemplate(
                template=transform_query_prompt,
                input_variables=["user_query", "chat_history"],
            ) | self.llm_model.with_structured_output(transform_question_structure)
        except Exception as err:
            raise RuntimeError(f"Pipeline creation failed due to: {err}")
