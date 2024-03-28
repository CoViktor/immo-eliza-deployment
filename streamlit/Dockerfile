# Python image
FROM python:3.10

# Working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the Streamlit app file into the container
COPY streamlit_app.py .

# Expose the port that Streamlit listens on
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "8501"]