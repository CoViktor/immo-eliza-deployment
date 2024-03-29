from joblib import load
from fastapi import HTTPException
import pandas as pd
from statsmodels.tools import add_constant


def load_training(type: str):
    """
    Loads the machine learning model, encoder, scaler, and column order based
    on the specified property type.

    Parameters:
    - type (str): The type of the property for which the model and related
    objects are to be loaded. Expected values are 'house' or 'apartment',
    case-insensitive.

    Returns:
    - tuple: A tuple containing the loaded model, encoder, scaler, and column
    order necessary for preprocessing and prediction.
    """
    typing = type.upper()
    model = load(f'./models/{typing}_trained_mlr_model.joblib') 
    encoder = load(f'./models/{typing}_encoder.joblib')
    scaler = load(f'./models/{typing}_scaler.joblib')
    column_order = load(f'./models/{typing}_columns.joblib')

    return model, encoder, scaler, column_order


def preprocess_input_data(input_data, propertytype='house'):
    """
    Preprocesses the input data for prediction based on the specified property
    type by encoding categorical features, scaling numerical features, and
    ensuring the data matches the expected column order.

    Parameters:
    - input_data (dict): The input data to be preprocessed.
    - propertytype (str, optional): The type of property ('house' or
    'apartment'). Defaults to 'house'.

    Returns:
    - tuple: A tuple containing the preprocessed DataFrame and the loaded
    model for the specified property type.
    """
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
    """
    Predicts the price of a property based on the provided input data.

    Parameters:
    - input_data (dict): The input data for which the prediction is to be made.

    Returns:
    - float: The predicted price of the property, rounded to two decimal
    places.

    Raises:
    - HTTPException: An exception is raised with status code 500 if any errors
    occur during the prediction process.
    """
    try:
        property_type = input_data['PropertyType']

        processed_data, model = preprocess_input_data(input_data, property_type)
        processed_data_with_const = add_constant(processed_data, has_constant='add')
        prediction = model.predict(processed_data_with_const)

        return round(prediction[0], 2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))