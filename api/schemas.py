from pydantic import BaseModel, conint, confloat
from typing import Optional


class InputData(BaseModel):
    """
    A Pydantic model representing the input data for a property price
    prediction request.

    Attributes:
        PostalZone (str): The postal zone of the property as a string.
        PropertyType (str): The type of property (e.g., 'House', 'Apartment').
        PropertySubType (str): The subtype of the property (e.g., 'Villa', 'Duplex').
        ConstructionYear (conint(ge=0)): The year of construction of the property.
        BedroomCount (Optional[conint(ge=0)]): The number of bedrooms in the property, if applicable.
        LivingArea (Optional[conint(ge=0)]): The living area of the property in square meters, if applicable.
        Furnished (Optional[int]): Indicates whether the property is furnished (1) or not (0), if applicable.
        Fireplace (Optional[int]): Indicates whether the property has a fireplace (1) or not (0), if applicable.
        Terrace (Optional[int]): Indicates whether the property has a terrace (1) or not (0), if applicable.
        Garden (Optional[int]): Indicates whether the property has a garden (1) or not (0), if applicable.
        GardenArea (Optional[conint(ge=0)]): The area of the garden in square meters, if applicable.
        Facades (Optional[conint(ge=0)]): The number of facades of the property, if applicable.
        SwimmingPool (Optional[int]): Indicates whether the property has a swimming pool (1) or not (0), if applicable.
        Condition (str): The condition of the property (e.g., 'New', 'To be renovated').
        EnergyConsumptionPerSqm (Optional[confloat(ge=0)]): The energy consumption per square meter, if applicable.
    """
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
    """
    A Pydantic model representing the output data of a property price prediction.

    Attributes:
        prediction (Optional[float]): The predicted price of the property, if available.
        status_code (Optional[int]): The status code indicating the outcome of the prediction operation, if applicable.
    """
    prediction: Optional[float] = None
    status_code: Optional[int] = None