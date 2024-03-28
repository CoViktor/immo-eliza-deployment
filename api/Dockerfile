# Python image
FROM python:3.10

# Working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application
COPY . /app

# Run the application using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]