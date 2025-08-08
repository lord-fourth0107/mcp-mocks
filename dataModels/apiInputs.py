from pydantic import BaseModel, Field, UUID4, HttpUrl, model_validator
from pydantic_csv import BasemodelCSVReader
from typing import Optional, Literal
from datetime import datetime
from dataModels.baseInput import UserInput, MetaData
class CSVFile(BaseModel):
    fileUrl: HttpUrl = Field(None, description="URL of the CSV file")

class Options(BaseModel):
    units: Optional[Literal["sqm", "sqft"]] = Field(default="sqm")
    language: Optional[str] = Field(None)
    strictMode: Optional[bool] = Field(default=False)

class Layers(BaseModel):
    wallsLayer: str = Field("WALLS", description="Name of the walls layer")
    roomsLayer: str = Field("ROOMS", description="Name of the rooms layer")
    coresLayer: str = Field("CORES", description="Name of the cores layer")
    circulationLayer: str = Field("CIRCULATION", description="Name of the circulation layer")

class JobOptions(Options):
    fileFormat: Literal["DXF", "IFC"] = Field("DXF", description="Format of the output file.")
    layers: Layers = Field(None, description="Layers to be included in the output file.")
    unit: Literal["m", "ft"] = Field("m", description="Unit of measurement for the output file.")
    includeSchedule: bool = Field(False, description="Whether to include the schedule in the output file.")

class TABSInput(UserInput):
    action: Literal["create", "update"]
    prompt: str
    csvFile: Optional[CSVFile] = None
    options: Optional[Options] = None 
    metadata: Optional[MetaData] = None



class FLANEInput(UserInput):
    options: Optional[JobOptions] = Field(None, description="Options for the job")

class BubbleInput(UserInput):
    options: Optional[Options] = None
    metaData: Optional[MetaData] =  None

# class UserInput(BaseInput):
#      userInput : str = Field(...,description = "Input from the user in plain english describing the task to be done by copilot app")




