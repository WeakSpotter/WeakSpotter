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
    git \
    bsdmainutils \
    && rm -rf /var/lib/apt/lists/*


# Create a non-root user and group
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Installer theHarvester et configurer son répertoire
RUN git clone https://github.com/laramies/theHarvester /opt/theHarvester \
    && pip install --no-cache-dir -r /opt/theHarvester/requirements/base.txt \
    && ln -s /opt/theHarvester/theHarvester.py /usr/local/bin/theHarvester \
    && mkdir -p /home/appuser/.theHarvester \
    && chown -R appuser:appuser /home/appuser


# Créer le répertoire requis par theHarvester
RUN mkdir -p /home/appuser/.theHarvester && chown -R appuser:appuser /home/appuser

# Installer Nikto depuis GitHub
RUN git clone https://github.com/sullo/nikto.git /opt/nikto \
    && ln -s /opt/nikto/program/nikto.pl /usr/local/bin/nikto

# Installer CMSmap
RUN git clone https://github.com/Dionach/CMSmap.git /opt/cmsmap \
    && ln -s /opt/cmsmap/cmsmap.py /usr/local/bin/cmsmap

# Installer SearchSploit
RUN git clone https://github.com/offensive-security/exploitdb.git /opt/exploitdb \
    && ln -s /opt/exploitdb/searchsploit /usr/local/bin/searchsploit

# Installer SQLMap
RUN git clone https://github.com/sqlmapproject/sqlmap.git /opt/sqlmap \
    && ln -s /opt/sqlmap/sqlmap.py /usr/local/bin/sqlmap

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY ./app /code/app
COPY requirements.txt /code/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Change ownership of the working directory
RUN chown -R appuser:appuser /code

# Switch to non-root user
USER appuser

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
