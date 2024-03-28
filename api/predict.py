from joblib import load
from fastapi import HTTPException
import pandas as pd
from statsmodels.tools import add_constant


def load_training(type: str):
    typing = type.upper()
    model = load(f'./models/{typing}_trained_mlr_model.joblib') 
    encoder = load(f'./models/{typing}_encoder.joblib')
    scaler = load(f'./models/{typing}_scaler.joblib')
    column_order = load(f'./models/{typing}_columns.joblib')

    return model, encoder, scaler, column_order


def preprocess_input_data(input_data, propertytype='house'):
    model, encoder, scaler, column_order = load_training(propertytype)
    df = pd.DataFrame([input_data])
    
    categorical_features = df.select_dtypes(include=['object']).columns
    encoded_features = encoder.transform(df[categorical_features]).toarray()
    encoded_features_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_features))
    df = df.drop(columns=categorical_features)
    df = pd.concat([df.reset_index(drop=True), encoded_features_df.reset_index(drop=True)], axis=1)
    numeric_features = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_features] = scaler.transform(df[numeric_features])
    missing_cols = set(column_order) - set(df.columns)
    for c in missing_cols:
        df[c] = 0

    df = df[column_order]

    return df, model


def predict_method(input_data):
    try:
        property_type = input_data['PropertyType']

        processed_data, model = preprocess_input_data(input_data, property_type)
        processed_data_with_const = add_constant(processed_data, has_constant='add')
        prediction = model.predict(processed_data_with_const)

        return round(prediction[0], 2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))