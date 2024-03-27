from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint, confloat
from typing import Optional
from predict import predict_method

app = FastAPI()

class InputData(BaseModel):
    PostalZone: str  # Extracted from the PostalCode, likely the first few characters
    PropertyType: str  # e.g., 'house', 'apartment'
    PropertySubType: str  # e.g., 'bungalow', 'villa', etc.
    ConstructionYear: Optional[conint(ge=0)] = None  # Assuming a positive integer or None
    BedroomCount: Optional[conint(ge=0)] = None
    LivingArea: Optional[conint(ge=0)] = None
    Furnished: Optional[bool] = None
    Fireplace: Optional[bool] = None
    Terrace: Optional[bool] = None
    Garden: Optional[bool] = None
    GardenArea: Optional[conint(ge=0)] = None
    Facades: Optional[conint(ge=0)] = None
    SwimmingPool: Optional[bool] = None
    Condition: str  # This might be restricted to certain values like 'new', 'good', 'renovate'
    EnergyConsumptionPerSqm: Optional[confloat(ge=0)] = None  # Assuming a positive float or None


class OutputData(BaseModel):
    prediction: Optional[float] = None
    status_code: Optional[int] = None


@app.get("/", tags=["root"])
async def root():
    """Route that return 'alive' if the server runs."""
    return {"Status": "alive"}

@app.get("/test", tags=["testing"])
async def predict(user: str = "Anonymous"):
    """Route that will return 'hello {user}'."""
    return {"Message": f"Hello {user}!"}

@app.post("/predict", response_model=OutputData, tags=["predict"])
async def predict(input: InputData):
    try:
        # Convert input to the format your prediction function expects
        input_dict = input.dict()
        prediction = predict_method(input_dict)
        
        return OutputData(prediction=prediction, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
