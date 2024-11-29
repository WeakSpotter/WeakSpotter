# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Add commit hash as an environment variable
ARG COMMIT_HASH
ENV COMMIT_HASH=${COMMIT_HASH}

RUN mkdir -p /data && chmod 777 /data

RUN apt-get update && apt-get install -y \
    curl \
    dnsutils \
    whois \
    nmap \
    git \
    bsdmainutils \
    && rm -rf /var/lib/apt/lists/*

# Installer setuptools et wheel (prérequis pour setup.py)
RUN pip install --no-cache-dir setuptools wheel

# Create a non-root user and group
RUN groupadd -r appuser && useradd -r -g appuser appuser


# Installer theHarvester et configurer son répertoire
RUN git clone https://github.com/laramies/theHarvester /opt/theHarvester \
    && pip install --no-cache-dir -r /opt/theHarvester/requirements/base.txt \
    && ln -sf /opt/theHarvester/theHarvester.py /usr/local/bin/theHarvester \
    && mkdir -p /home/appuser/.theHarvester \
    && chown -R appuser:appuser /home/appuser

# Installer Nikto depuis GitHub
RUN git clone https://github.com/sullo/nikto.git /opt/nikto \
    && ln -sf /opt/nikto/program/nikto.pl /usr/local/bin/nikto


#Install exploitdb
RUN git clone https://gitlab.com/exploit-database/exploitdb.git /opt/exploitdb \
    && ln -sf /opt/exploitdb/searchsploit /usr/local/bin/searchsploit

RUN git config --global --add safe.directory /opt/exploitdb

# Installer CMSmap
RUN git clone https://github.com/Dionach/CMSmap.git /opt/cmsmap \
    && cd /opt/cmsmap \
    && sed -i 's|edbtype = apt|edbtype = GIT|' /opt/cmsmap/cmsmap/cmsmap.conf \
    && sed -i 's|edbpath = /usr/share/exploitdb/|edbpath = /opt/exploitdb/|' /opt/cmsmap/cmsmap/cmsmap.conf \
    && chown -R appuser:appuser /opt/cmsmap \
    && pip3 install . 

# Installer SQLMap
RUN git clone https://github.com/sqlmapproject/sqlmap.git /opt/sqlmap \
    && ln -sf /opt/sqlmap/sqlmap.py /usr/local/bin/sqlmap

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY ./app /code/app
COPY requirements.txt /code/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Change ownership of the working directory
RUN chown -R appuser:appuser /code

RUN chown -R appuser:appuser /usr/local/lib/python3.12/site-packages/cmsmap/

# Switch to non-root user
USER appuser

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
