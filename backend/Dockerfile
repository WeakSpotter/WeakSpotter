# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Add commit hash as an environment variable
ARG COMMIT_HASH
ENV COMMIT_HASH=${COMMIT_HASH}

RUN apt-get update && apt-get install -y \
    curl \
    dnsutils \
    whois \
    nmap \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY ./app /code/app
COPY requirements.txt /code/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
