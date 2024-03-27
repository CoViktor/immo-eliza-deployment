# Start from the Python 3.10 official image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application
COPY . /app

# Command to run the application using uvicorn
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0"]