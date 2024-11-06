FROM python:3.8-slim
WORKDIR /usr/src/app
COPY app/ .

# Installer curl, Flask, et whatweb
RUN apt-get update && \
    apt-get install -y curl whatweb && \
    pip install flask

EXPOSE 5000
CMD ["python", "analyzer.py"]
