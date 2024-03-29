from fastapi import FastAPI, HTTPException
from predict import predict_method
from schemas import InputData, OutputData

app = FastAPI()


@app.get("/", tags=["root"])
async def root():
    """Route that return 'alive' if the server runs."""
    return {"Status": "alive"}


@app.post("/predict", response_model=OutputData, tags=["predict"])
async def predict_price(input: InputData):
    """
    Receives input data as per the InputData model, uses the `predict_method`
    to predict a price, and returns the prediction and status code.

    Raises HTTPException with status code 500 if any errors occur during
    prediction.
    """
    try:
        input_dict = input.dict()
        prediction = predict_method(input_dict)
        return OutputData(prediction=prediction, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
