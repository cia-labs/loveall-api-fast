# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Command to run the uvicorn server
# CMD ["uvicorn", "manager:app", "--host", "0.0.0.0", "--port", "9000"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "14000", "--reload"]