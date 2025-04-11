from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os

from response_structures import final_response_structure
from prompts import response_generation_prompt


class response_generation_agent_pipeline:
    """
    Responsible for generating the final response based on provided data
    """

    def __init__(self) -> None:

        self.llm_model = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL"), api_key=os.getenv("OPENAI_KEY")
        )

        self.response_generation_pipeline = self._setup_pipeline_structure()

    def execute_agent(self, **kwargs):
        """kwargs param :
        sql_output (str): claims database output
        user_query(str)   : user question.
        """

        return self.response_generation_pipeline.invoke(
            {
                "sql_output": kwargs["sql_output"],
                "user_question": kwargs["user_question"],
            }
        )

    def _setup_pipeline_structure(self):
        """Sets up the response generation chain using modular components."""
        final_response_prompt_template = PromptTemplate(
            template=response_generation_prompt,
            input_variables=["sql_output", "user_question"],
        )
        return final_response_prompt_template | self.llm_model.with_structured_output(
            final_response_structure
        )
