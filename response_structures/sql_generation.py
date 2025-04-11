from pydantic import BaseModel, Field


class sql_generator_structure(BaseModel):
    """
    It used for generating SQL query for given database schema. 

    """
    sql_query: str | None = Field(description = """SQL query generated based on provided table schema.""")
    is_not_related: bool = Field(description = """A boolean flag that should be marked true, when question is not releted to the schema and insurance claims.""")
    message:str|None = Field(description="Message from assistant if the question from user in not related to insurance claims or text-to-sql task.")
