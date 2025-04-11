from pydantic import BaseModel, Field


class transform_question_structure(BaseModel):
    """Refines and enhances user question to make it more informative and technically detailed. 
    """
    transformed_question:str | None = Field(description="Transformed user question to be used for SQL code generation only.")
    is_not_related: bool = Field(description = """Should be marked true if question is not related to text-to-sql task or related to insurance claims.""")
    message:str|None = Field(description="The message to be sent to the user. Message should be formal and polite.")