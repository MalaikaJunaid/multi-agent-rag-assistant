# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install fastapi uvicorn

# Copy the entire project into the container
COPY . .

# Expose the port the FastAPI server runs on
EXPOSE 8000

# Command to run the REST API using uvicorn
CMD ["uvicorn", "backend.api.server:app", "--host", "0.0.0.0", "--port", "8000"]