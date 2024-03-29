import streamlit as st
import requests
import json

st.title('Immo Eliza') 
st.write('Fill in the form below to predict the price of your dream house!')

PostalZone = st.text_input('What are the 2 first numbers of the postal code (Postal zone)? (e.g. 90):')
if PostalZone and (not PostalZone.isdigit() or len(PostalZone) != 2):
    st.error('Postal zone must be exactly 2 digits.')
PropertyType = st.selectbox('Property type:', ('House', 'Apartment'))
if PropertyType == 'House':
    PropertySubType = st.selectbox('Subtype:', ('House', 'Villa', 'Town_House', 'Apartment_Block', 'Mixed_Use_Building', 'Bungalow ', 'Mansion', 'Exceptional_Property', 'Country_Cottage', 'Chalet', 'Manor_House', 'Other_Property', 'Farmhouse'))
elif PropertyType == 'Apartment':
    PropertySubType = st.selectbox('Subtype:', ('Apartment', 'Ground_Floor', 'Duplex', 'Flat_Studio', 'Penthouse', 'Service_Flat', 'Loft', 'Kot', 'Triplex'))
else:
    PropertySubType = st.selectbox('Pick one:', ('Option 1', 'Option 2', 'Option 3'))
ConstructionYear = st.text_input('Construction year:')
if ConstructionYear and len(ConstructionYear) != 4:
    st.error('Construction year must be exactly 4 digits.')
ConstructionYear = int(ConstructionYear) if ConstructionYear else None
if ConstructionYear and ConstructionYear < 1800:
    st.error('Construction year to old for price estimation with this model.')
if ConstructionYear and ConstructionYear > 2030:
    st.error('Construction year to new for price estimation with this model.')
BedroomCount = st.slider('Amount of bedrooms:', 0, 10)
LivingArea = st.slider('Living area in m²:', 0, 1000)
Furnished = st.checkbox('Is furnished?')
Fireplace = st.checkbox('Has a fireplace?')
Terrace = st.checkbox('Has a terrace?')
Garden = st.checkbox('Has a garden?')
if Garden:
    GardenArea = st.slider('Garden area in m²:', 0, 800)
else:
    GardenArea = 0
Facades = st.slider('Amount of facades:', 0, 10)
SwimmingPool = st.checkbox('Has a swimming pool?')
Condition = st.radio('Pick one:', ('Good', 'As_New', 'To_Be_Done_Up', 'Just_Renovated', 'To_Renovate', 'To_Restore'))
EnergyConsumptionPerSqm = st.slider('Energy consumption per square meter:', 0.0, 1000.0)


url = 'https://immo-eliza-deployment-api.onrender.com/predict'
data = {
    "PostalZone": PostalZone,
    "PropertyType": PropertyType,
    "PropertySubType": PropertySubType,
    "ConstructionYear": ConstructionYear,
    "BedroomCount": BedroomCount,
    "LivingArea": LivingArea,
    "Furnished": Furnished,
    "Fireplace": Fireplace,
    "Terrace": Terrace,
    "Garden": Garden,
    "GardenArea": GardenArea,
    "Facades": Facades,
    "SwimmingPool": SwimmingPool,
    "Condition": Condition,
    "EnergyConsumptionPerSqm": EnergyConsumptionPerSqm
}
headers = {'Content-type': 'application/json'}


required_fields_filled = PostalZone and ConstructionYear is not None and len(PostalZone) == 2 and PostalZone.isdigit()
if required_fields_filled:
    if st.button("Click me to get a price estimation!"):
        try:
            url = 'https://immo-eliza-deployment-api.onrender.com/predict'
            headers = {'Content-type': 'application/json'}
            response = requests.post(url, data=json.dumps(data), headers=headers)
            prediction = response.json()["prediction"]
            st.subheader("Result:")
            st.write(f"The property will probably cost about: €{round((prediction/1000))}.000")
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.write("Please fill in all required fields to get a price estimation.")
