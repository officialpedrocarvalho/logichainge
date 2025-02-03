# Dockerfile

# Use a Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into the container
COPY . /app/

# Expose port
EXPOSE 8000

# Command to run Django application
CMD ["gunicorn", "app.wsgi:application"]
