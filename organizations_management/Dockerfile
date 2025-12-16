# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables to avoid Python writing pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install build dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements.txt first to leverage Docker's cache
COPY requirements.txt /app/

# Upgrade pip and setuptools before installing dependencies
RUN pip install --upgrade pip setuptools

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org -r requirements.txt

# Now copy the rest of your application code into the container
COPY . /app

# Expose the port that FastAPI will run on
EXPOSE 8000

# Run FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
