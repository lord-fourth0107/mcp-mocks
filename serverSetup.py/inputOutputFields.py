from pydantic import BaseModel, Field, UUID4, HttpUrl
from typing import List
class Input(BaseModel):
    requestId :UUID4 = Field(...,description="Request ID")
    userId : str = Field(...,description="User ID") 
    naturalLanguageInput : str = Field(...,description="Natural Language Input")

class Output(BaseModel):
    requestId :UUID4 = Field(...,description="Request ID")
    userId : str = Field(...,description="User ID") 
    status : str = Field(...,description="Status")
    response : str = Field(...,description="Response")
    apiUrl :HttpUrl=Field(...,description="API URL")
    