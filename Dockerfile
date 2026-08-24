# Use the official Python image as a base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port that Uvicorn runs on
EXPOSE 8000

# Define the command to run your app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
