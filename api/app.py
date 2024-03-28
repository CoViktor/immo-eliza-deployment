from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint, confloat
from typing import Optional
from predict import predict_method

app = FastAPI()
# Run from inside the api folder: uvicorn app:app --reload

class InputData(BaseModel):
    PostalZone: str  # 2 first numbers of postalcode
    PropertyType: str  # e.g. 'House', 'Apartment'
    PropertySubType: str  # e.g. House: 'House', 'Villa', 'Town_House', 'Apartment_Block', 'Mixed_Use_Building', 'Bungalow ', 'Mansion', 'Exceptional_Property', 'Country_Cottage', 'Chalet', 'Manor_House', 'Other_Property', 'Farmhouse'
    ConstructionYear: Optional[conint(ge=0)] = None  # e.g. Apartment: 'Apartment', 'Ground_Floor', 'Duplex', 'Flat_Studio', 'Penthouse', 'Service_Flat', 'Loft', 'Kot', 'Triplex'
    BedroomCount: Optional[conint(ge=0)] = None
    LivingArea: Optional[conint(ge=0)] = None
    Furnished: Optional[int] = None
    Fireplace: Optional[int] = None
    Terrace: Optional[int] = None
    Garden: Optional[int] = None
    GardenArea: Optional[conint(ge=0)] = None
    Facades: Optional[conint(ge=0)] = None
    SwimmingPool: Optional[int] = None
    Condition: str  # e.g. 'Good', 'As_New', 'To_Be_Done_Up', 'Just_Renovated', 'To_Renovate', 'To_Restore'
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
async def predict_price(input: InputData):
    try:
        # Convert input to the format your prediction function expects
        input_dict = input.dict()
        prediction = predict_method(input_dict)

        # formatted_prediction = f"€{prediction}"
        # change below if needed
        return OutputData(prediction=prediction, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
