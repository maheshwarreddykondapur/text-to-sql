from langchain_openai import ChatOpenAI
import os

from response_structures import sql_generator_structure, sql_validator_structure
from langchain_core.prompts import PromptTemplate
from prompts import sql_query_generation_prompt, sql_query_validator_prompt


class sql_agent_pipeline:
    def __init__(self, **kwargs) -> None:

        self.llm_model = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL"), api_key=os.getenv("OPENAI_KEY"), temperature=None
        )

        self.sql_generation_llm, self.sql_validation_llm = (
            self.structure_llm_initilization()
        )

        self.sql_generation_pipeline = self.generation_llm_pipeline()
        self.sql_validation_pipeline = self.validation_llm_pipeline()

        if isinstance(self.sql_validation_pipeline, str):
            raise AttributeError(
                f"Not able to initilize the mssql server due to {self.llm_validative_pipeline}"
            )

        if isinstance(self.sql_generation_pipeline, str):
            raise AttributeError(
                f"Not able to initilize the mssql server due to {self.llm_generative_pipeline}"
            )

    def execute_agent(self, **kwargs):

        return self.sql_generation_pipeline.invoke({"user_query": kwargs["user_query"]})

    def execute_validation_agent(self, user_query: str, sql_query: str):

        return self.sql_validation_pipeline.invoke(
            {"user_query": user_query, "sql_query": sql_query}
        )

    def structure_llm_initilization(self):
        generation = self.llm_model.with_structured_output(sql_generator_structure)
        validation = self.llm_model.with_structured_output(sql_validator_structure)
        return generation, validation

    def generation_llm_pipeline(self):
        """Sets up the sql generation chain using modular components."""
        sql_prompt_template = PromptTemplate(
            template=sql_query_generation_prompt, input_variables=["user_query"]
        )
        return sql_prompt_template | self.sql_generation_llm

    def validation_llm_pipeline(self):
        """Sets up the sql validation chain using modular components."""
        sql_val_prompt_template = PromptTemplate(
            template=sql_query_validator_prompt,
            input_variables=["user_query", "sql_query"],
        )
        return sql_val_prompt_template | self.sql_validation_llm
