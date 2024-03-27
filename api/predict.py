from joblib import load
from fastapi import HTTPException
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# Check for house or appartment split
model = load('./api/models/HOUSE_trained_mlr_model.joblib') 
encoder = load('./api/models/HOUSE_encoder.joblib')
scaler = load('./api/models/HOUSE_scaler.joblib')
column_order = load('./api/models/HOUSE_columns.joblib')

print(type(model))

def preprocess_input_data(input_data):
    df = pd.DataFrame([input_data])
    # Apply one-hot encoding
    # For the incoming data, we assume we need to transform only, not fit_transform
    categorical_features = df.select_dtypes(include=['object']).columns
    encoded_features = encoder.transform(df[categorical_features]).toarray()
    encoded_features_df = pd.DataFrame(encoded_features,
                                       columns=encoder.get_feature_names_out(categorical_features))
    # Drop original categorical columns
    df = df.drop(columns=categorical_features)
    # Concatenate the one-hot encoded columns back to the DataFrame
    df = pd.concat([df, encoded_features_df], axis=1)
    # Apply scaling
    numeric_features = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_features] = scaler.transform(df[numeric_features])
    # Ensure the column order matches the training data
    df = df.reindex(columns=column_order, fill_value=0)

    return df

def predict(input_data):
    # Note that this function should not return OutputData; it should return the prediction value
    try:
        # Convert the input data from Pydantic model to a format suitable for prediction
        processed_data = preprocess_input_data(input_data)
        prediction = model.predict(processed_data)
        return prediction
    except Exception as e:
        # Handle errors gracefully
        raise HTTPException(status_code=500, detail=str(e))
    



#  """"A few notes on your code:
#  You should confirm that the categorical_features and 
#  numeric_features lists are consistent with those used during the training of 
#  your model. You may need to define these explicitly if they don't match.
#  """"