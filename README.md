# immo-eliza-deployment

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white)

This project is a web-based application for predicting real estate prices using a multiple linear regression model, designed to provide instant property price estimations based on user input. The backend API, built with FastAPI, processes prediction requests, while the frontend, created with Streamlit, offers an intuitive interface for users to input property details.

<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT01IkDyU9bH5UomGTvFmkPvs_hv57RztooaQ&s" width="400" height="auto"/>

## 🚀 Deployment

Both the FastAPI backend and the Streamlit frontend are deployed on Render, containerized with Docker.

## 📂 Repository Structure
```
.
├── api/
│ ├── models/
│   └──  *.joblib
│ ├── app.py
│ ├── Dockerfile
│ ├── predict.py
│ ├── requirements.txt
│ └── schemas.py
├── streamlit/
│ ├── Dockerfile
│ ├── requirements.txt
│ └── streamlit_app.py
├── .gitignore
└── README.md
```

## 🏗️ Setup

### Requirements

Both the API and Streamlit applications are containerized and deployed, removing the need for local setup for usage. You can just access the link below for the frontend app. However, if you wish to run them locally or contribute, the dependencies in the `requirements.txt` files are required. More information in the **local development** section below.

## 🔮 Usage
### Access the Streamlit App:
Open your web browser and navigate to the [Streamlit app's URL deployed on Render](https://immo-eliza-deployment-streamlit.onrender.com/).

### Enter Property Details:
Fill in the form with the required property details such as postal zone, property type, construction year, etc.

### Get Price Estimation:
Click on the "Get Price Estimation" button to submit your request. The predicted property price will be displayed shortly.

## 📚 Additional Information
For more details on the prediction models, including its accuracy and how it was trained, please refer to the [model card](https://github.com/CoViktor/immo-eliza-ml/blob/main/modelscard.md).

## 🛠️ Local Development

### FastAPI Backend

To run the FastAPI backend locally for development purposes, navigate to the `api/` directory and use `uvicorn` to serve the application. Ensure you have `uvicorn` installed, or install it using pip:

```sh
pip install uvicorn
```
Then, start the FastAPI server with:
```
uvicorn api/app:app --reload
```
The **--reload** flag enables auto-reload so the server will restart after code changes. By default, the FastAPI app will be available at: <br> **http://127.0.0.1:8000**

### Streamlit Frontend
To run the Streamlit app locally, navigate to the streamlit/ directory. Make sure Streamlit is installed, or install it using pip:
```
pip install streamlit
```
Then, start the Streamlit app with:
```
streamlit run streamlit/streamlit_app.py
```
Streamlit will automatically open the application in your default web browser, typically available at: <br> **http://localhost:8501**



# 📫 Contact
For questions, contributions, or collaborations, find me on [LinkedIn](https://www.linkedin.com/in/viktor-cosaert/).