# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install any dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Set the environment variable for Flask to run in production
ENV FLASK_ENV=production

# Run the Flask app using gunicorn (for production)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "service.__init__:app"]
