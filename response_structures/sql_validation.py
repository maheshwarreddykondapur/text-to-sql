from pydantic import BaseModel, Field,StrictBool

class sql_validator_structure(BaseModel):
    valid_query:bool = Field(description = "Marked true if the provided query is valid else it will be false.")
    sql_query:str|None = Field(description = "Updated SQLlite query if input sql query is invalid else it will be None.")

