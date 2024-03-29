from pydantic import BaseModel, conint, confloat
from typing import Optional


class InputData(BaseModel):
    PostalZone: str  
    PropertyType: str  
    PropertySubType: str  
    ConstructionYear: conint(ge=0)
    BedroomCount: Optional[conint(ge=0)] = None
    LivingArea: Optional[conint(ge=0)] = None
    Furnished: Optional[int] = None
    Fireplace: Optional[int] = None
    Terrace: Optional[int] = None
    Garden: Optional[int] = None
    GardenArea: Optional[conint(ge=0)] = None
    Facades: Optional[conint(ge=0)] = None
    SwimmingPool: Optional[int] = None
    Condition: str
    EnergyConsumptionPerSqm: Optional[confloat(ge=0)] = None


class OutputData(BaseModel):
    prediction: Optional[float] = None
    status_code: Optional[int] = None