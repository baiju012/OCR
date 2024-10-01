# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Tesseract-OCR
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get clean

# Copy the Tesseract config to the container (if any)
#COPY tessdata/ /usr/share/tesseract-ocr/4.00/tessdata/

# Expose port 5000 to allow access to the app
EXPOSE 5000

# Define environment variable to disable buffering (useful for logging)
ENV PYTHONUNBUFFERED=1

# Run the Flask app (or you can use gunicorn for production)
CMD ["python", "app.py"]
