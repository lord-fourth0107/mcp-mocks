from pydantic import BaseModel,Field,UUID4,HttpUrl
from typing import Optional,List, Annotated
from datetime import datetime
from enum import Enum

class Units(str,Enum):
    m = "m"
    ft = "ft"

class MetaData(BaseModel):
    userId : Optional[str] = Field(None, description="ID of the user who submitted the request")
    timeStamp : Optional[datetime] = Field(None, description="Client timestamp for the request (ISO 8601)")

"""
Options is the input format for all API requests.
"""   
class Options(BaseModel):
    layerName : str = Field(default="BUILDABLE_AREA",description="Name of the new buildable-area layer")
    units : Units = Field(default="m",description="Units of the lot file")
"""
BaseInput is the input format for all API requests.
"""
class BaseInput(BaseModel):
    projectId: str = Field(...,description= "ID of the project context in which the lot and code rules are stored")
    requestId: UUID4 = Field(..., description="ID of the request")
    studyId : str = Field(...,description= "ID of the study context. Each project has one or more studies")
    userId : str = Field(...,description= "ID of the user who submitted the request")