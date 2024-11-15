import requests

from app.models.scan import Scan

def scan(scan: Scan) -> dict:
    try:
        response = requests.get(scan.url)
        status = "up" if response.status_code == 200 else "down"
    except requests.exceptions.RequestException:
        status = "down"

    return {"status": status}
