import streamlit as st
import requests
import json

st.title('Immo Eliza') 
st.write('Fill in the form below to predict the price of your dream house!')

PostalZone = st.text_input('What are the 2 first numbers of the postal code (Postal zone)?')
if PostalZone and (not PostalZone.isdigit() or len(PostalZone) != 2):
    st.error('Postal zone must be exactly 2 digits, ranging from 10 to 99.')
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
if ConstructionYear and ConstructionYear < 1750:
    st.error('Construction year to old for price estimation with this model.')
if ConstructionYear and ConstructionYear > 2030:
    st.error('Construction year to new for price estimation with this model.')
if PropertyType == 'House':
    BedroomCount = st.slider('Amount of bedrooms:', 1, 7)
    LivingArea = st.slider('Living area in m²:', 25, 400)
    Facades = st.slider('Amount of facades:', 1, 8)
    Furnished = st.checkbox('Is furnished?')
    Fireplace = st.checkbox('Has a fireplace?')
    Terrace = st.checkbox('Has a terrace?')
    Garden = st.checkbox('Has a garden?')
    if Garden:
        GardenArea = st.slider('Garden area in m²:', 0, 1500)
    else:
        GardenArea = 0
    SwimmingPool = st.checkbox('Has a swimming pool?')
    Condition = st.radio('State of the property:', ('Good', 'As_New', 'Just_Renovated', 'To_Renovate', 'To_Be_Done_Up', 'To_Restore'))
    EnergyConsumptionPerSqm = st.slider('Energy consumption per square meter ([Click here if you only know the EPC-value](https://static.standaard.be/Assets/Images_Upload/2024/01/31/M_EPC_1.png)):', 0, 1000)

elif PropertyType == 'Apartment':
    BedroomCount = st.slider('Amount of bedrooms:', 0, 5)
    LivingArea = st.slider('Living area in m²:', 10, 200)
    Facades = st.slider('Amount of facades:', 1, 5)
    Furnished = st.checkbox('Is furnished?')
    Fireplace = st.checkbox('Has a fireplace?')
    Terrace = st.checkbox('Has a terrace?')
    Garden = st.checkbox('Has a garden?')
    GardenArea = 0
    SwimmingPool = st.checkbox('Has a swimming pool?')
    Condition = st.radio('State of the property:', ('Good', 'As_New', 'Just_Renovated', 'To_Renovate', 'To_Be_Done_Up', 'To_Restore'))
    EnergyConsumptionPerSqm = st.slider('Energy consumption per square meter ([Click here if you only know the EPC-value](https://static.standaard.be/Assets/Images_Upload/2024/01/31/M_EPC_1.png)):', 0, 500)
    

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
        if LivingArea == 0:
            st.error('Are you sure this property has no living area?')
        else:
            try:
                url = 'https://immo-eliza-deployment-api.onrender.com/predict'
                headers = {'Content-type': 'application/json'}
                response = requests.post(url, data=json.dumps(data), headers=headers)
                prediction = response.json()["prediction"]
                st.subheader("Result:")
                st.markdown(f"The property will probably cost about:<br>**€{round((prediction)/1000)}.000**", unsafe_allow_html=True)
                st.image('https://media1.tenor.com/m/9RC8mfWlbaQAAAAC/shut-up-and-take-my-money-philip-j-fry.gif')

                if PropertyType == 'House':
                    r2 = 0.726
                    rmse = 86
                elif PropertyType == 'Apartment':
                    r2 = 0.64
                    rmse = 67

                st.markdown(f"""
                <style>
                .small-font {{
                    font-size:12px;
                }}
                </style>
                <div class="small-font">
                    Disclaimer:<br> This prediction is based on data scraped from 
                            <a href="https://www.immoweb.be" target="_blank">www.immoweb.be</a>.<br> 
                            The used Multilinear Regression model has an R² of {r2} and an RMSE of {rmse}.000 euros.<br>
                            Please refer this <a href="https://github.com/CoViktor/immo-eliza-ml/blob/main/modelscard.md" target="_blank">model card</a> for more information.<br>
                            Find me on <a href="https://www.linkedin.com/in/viktor-cosaert/" target="_blank">LinkedIn</a>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.write("Please fill in all required fields to get a price estimation.")
