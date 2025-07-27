# Filename: backend/Dockerfile

# Use a lean Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy and install Python dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the backend code
COPY . /app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]