import subprocess
from typing import Any

from app.models.scan import Scan


def sanitize_url(url: str) -> str:
    if not url.startswith("http"):
        url = f"https://{url}"
    return url


def add_data(scan: Scan, key: str, value: Any):
    data = scan.data_dict
    data[key] = value
    scan.data_dict = data


def execute_command(command: str) -> list:
    """Executes a shell command and returns the output as a list of lines."""
    try:
        output = subprocess.check_output(command, shell=True).decode("utf-8").strip()
        return output.split("\n") if output else []
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {command}\nError: {e}")
        return []
