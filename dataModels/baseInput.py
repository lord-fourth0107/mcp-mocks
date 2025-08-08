from pydantic import BaseModel,Field,UUID4,HttpUrl
from typing import Optional,List, Annotated
from datetime import datetime
from enum import Enum

class Units(str,Enum):
    m = "m"
    ft = "ft"

class MetaData(BaseModel):
    userId : Optional[str] = Field(None)
    timeStamp : Optional[datetime] = Field(None)

"""
Options is the input format for all API requests.
"""   
class Options(BaseModel):
    layerName : str = Field(default="BUILDABLE_AREA")
    units : Units = Field(default="m")
"""
BaseInput is the input format for all API requests.
"""
class UserInput(BaseModel):
    projectId: str = Field(...)
    requestId: UUID4 = Field(...)
    userId : str = Field(...)
    userQuery : str = Field(None)