import subprocess
import xml.etree.ElementTree as ET

from app.models.scan import Scan


def nmap_scan(scan: Scan) -> (str, str):
    """Performs an Nmap scan on the domain."""
    domain = scan.data_dict.get("domain")
    if not domain:
        return "nmap", None

    command = f"nmap -sV {domain} -oX -"
    try:
        result = subprocess.check_output(command, shell=True).decode("utf-8")
        return "nmap", parse_nmap_output(result)
    except subprocess.CalledProcessError as e:
        print(f"Nmap scan failed for domain {domain}\nError: {e}")
        return "nmap", None


def parse_nmap_output(xml_output: str) -> dict:
    """Parses the Nmap XML output and returns a dictionary with relevant information."""
    root = ET.fromstring(xml_output)

    result = {"host": {"ip": None, "hostnames": [], "ports": []}}

    # Extract IP address
    address = root.find(".//address[@addrtype='ipv4']")
    if address is not None:
        result["host"]["ip"] = address.get("addr")

    # Extract hostnames
    hostnames = root.findall(".//hostname")
    for hostname in hostnames:
        result["host"]["hostnames"].append(hostname.get("name"))

    # Extract open ports and their details
    ports = root.findall(".//port")
    for port in ports:
        port_info = {
            "protocol": port.get("protocol"),
            "portid": port.get("portid"),
            "state": port.find(".//state").get("state"),
            "service": {
                "name": port.find(".//service").get("name"),
                "product": port.find(".//service").get("product"),
                "version": port.find(".//service").get("version"),
                "extrainfo": port.find(".//service").get("extrainfo"),
                "ostype": port.find(".//service").get("ostype"),
                "method": port.find(".//service").get("method"),
                "conf": port.find(".//service").get("conf"),
            },
        }
        result["host"]["ports"].append(port_info)

    return result
