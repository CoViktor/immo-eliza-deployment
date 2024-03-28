from joblib import load
from fastapi import HTTPException
import pandas as pd
from statsmodels.tools import add_constant


# Check for house or appartment split
model = load('./models/HOUSE_trained_mlr_model.joblib') 
encoder = load('./models/HOUSE_encoder.joblib')
scaler = load('./models/HOUSE_scaler.joblib')
column_order = load('./models/HOUSE_columns.joblib')

def preprocess_input_data(input_data):
    df = pd.DataFrame([input_data])
    # Apply one-hot encoding
    # For the incoming data, we assume we need to transform only, not fit_transform
    categorical_features = df.select_dtypes(include=['object']).columns
    encoded_features = encoder.transform(df[categorical_features]).toarray()
    encoded_features_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_features))
    # Drop original categorical columns
    df = df.drop(columns=categorical_features)
    # Concatenate encoded features
    df = pd.concat([df.reset_index(drop=True), encoded_features_df.reset_index(drop=True)], axis=1)
    # Scale numeric features
    numeric_features = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_features] = scaler.transform(df[numeric_features])

    # Ensure all columns are present
    missing_cols = set(column_order) - set(df.columns)
    for c in missing_cols:
        df[c] = 0

    df = df[column_order]

    return df

def predict_method(input_data):
    # Note that this function should not return OutputData; it should return the prediction value
    try:
        # Convert the input data from Pydantic model to a format suitable for prediction
        processed_data = preprocess_input_data(input_data)
        processed_data_with_const = add_constant(processed_data, has_constant='add')
        prediction = model.predict(processed_data_with_const)
        return round(prediction[0], 2)
    except Exception as e:
        # Handle errors gracefully
        raise HTTPException(status_code=500, detail=str(e))
    



#  """"A few notes on your code:
#  You should confirm that the categorical_features and 
#  numeric_features lists are consistent with those used during the training of 
#  your model. You may need to define these explicitly if they don't match.
#  """"