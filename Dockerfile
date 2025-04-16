# Use Python 3.9-slim as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Set the default user (optional, for security purposes)
RUN useradd --uid 1000 theia && chown -R theia /app

# Switch to the new user
USER theia

# Expose port 8080 (the default port for Gunicorn in this case)
EXPOSE 8080

# Command to run the application using Gunicorn
CMD ["gunicorn", "-w", "4", "wsgi:app"]
