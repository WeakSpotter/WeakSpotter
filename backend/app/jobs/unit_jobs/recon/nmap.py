import subprocess
import xml.etree.ElementTree as ET

from app.jobs.abstract_job import Job
from app.jobs.license import License


class NmapScanJob(Job):
    requirements = ["domain"]
    key = "nmap"
    name = "Nmap"
    license = License.NSPL

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
            # Initialize service element
            service = port.find(".//service")
            state = port.find(".//state")

            port_info = {
                "protocol": port.get("protocol"),
                "portid": port.get("portid"),
                "state": state.get("state") if state is not None else None,
                "service": {
                    "name": service.get("name") if service is not None else None,
                    "product": service.get("product") if service is not None else None,
                    "version": service.get("version") if service is not None else None,
                    "extrainfo": service.get("extrainfo")
                    if service is not None
                    else None,
                    "ostype": service.get("ostype") if service is not None else None,
                    "method": service.get("method") if service is not None else None,
                    "conf": service.get("conf") if service is not None else None,
                },
            }
            self.result["host"]["ports"].append(port_info)

    def score(self) -> float:
        return 0.0

    def definitions(self):
        return []
