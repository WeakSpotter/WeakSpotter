import subprocess
import xml.etree.ElementTree as ET

from app.jobs.abstract_job import Job


class NmapScanJob(Job):
    requirements = ["domain"]
    key = "nmap"
    name = "Nmap Scan"

    def run(self) -> None:
        domain = self._scan.data_dict.get("domain")

        command = f"nmap -sV {domain} -oX -"

        self._raw_output = subprocess.check_output(command, shell=True).decode("utf-8")

    def parse_results(self) -> None:
        root = ET.fromstring(self._raw_output)

        self.result = {"host": {"ip": None, "hostnames": [], "ports": []}}

        # Extract IP address
        address = root.find(".//address[@addrtype='ipv4']")
        if address is not None:
            self.result["host"]["ip"] = address.get("addr")

        # Extract hostnames
        hostnames = root.findall(".//hostname")
        for hostname in hostnames:
            self.result["host"]["hostnames"].append(hostname.get("name"))

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
            self.result["host"]["ports"].append(port_info)

    def score(self) -> float:
        return 0.0

    def definitions(self):
        return {}
