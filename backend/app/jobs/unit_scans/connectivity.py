import socket

import requests

from app.models.scan import Scan

def http_status(scan: Scan) -> dict:
    try:
        req = requests.get(scan.url)
        return {"status": req.status_code}
    except requests.exceptions.RequestException:
        return {"status": 0}

def ip(scan: Scan) -> dict:
    domain = scan.url.split("//")[-1]

    domain = domain.split("/")[0] if "/" in domain else domain

    try:
        return {"ip": socket.gethostbyname(domain)}
    except socket.gaierror:
        return {"ip": None}
