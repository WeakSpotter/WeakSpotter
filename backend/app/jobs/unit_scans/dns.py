import ipaddress
import subprocess
from urllib.parse import urlparse

import requests
from app.jobs.job import Job
from app.models.scan import Scan

CF_IPV4_LIST_URL = "https://www.cloudflare.com/ips-v4/"
CF_IPV6_LIST_URL = "https://www.cloudflare.com/ips-v6/"


class DomainExtractJob(Job):
    def __init__(self):
        super().__init__("Domain Extract", "domain", self.domain_extract)

    @staticmethod
    def domain_extract(scan: Scan) -> str:
        """Extracts the domain from the URL."""
        domain = urlparse(scan.url).netloc
        return domain


class WhoisJob(Job):
    def __init__(self):
        super().__init__("Whois", "whois", self.whois)

    @staticmethod
    def whois(scan: Scan) -> str:
        """Retrieves the WHOIS record for the domain."""
        domain = scan.data_dict.get("domain")
        if not domain:
            return None

        command = f"whois {domain}"
        try:
            result = subprocess.check_output(command, shell=True).decode("utf-8")
            return result
        except subprocess.CalledProcessError as e:
            print(f"WHOIS command failed for domain {domain}\nError: {e}")
            return None


class DNSRecordsJob(Job):
    def __init__(self):
        super().__init__("DNS Records", "dns_records", self.dns_records)

    @staticmethod
    def dns_records(scan: Scan) -> dict:
        """Retrieves the A, AAAA, and CNAME records for a domain using dig."""
        domain = scan.data_dict.get("domain")
        if not domain:
            return {}

        commands = {
            "a": f"dig +short {domain} A | grep '^[.0-9]*$'",
            "aaaa": f"dig +short {domain} AAAA | grep '^[0-9a-fA-F:]*$'",
            "cname": f"dig +short {domain} CNAME",
        }

        results = {key: execute_command(command) for key, command in commands.items()}
        return results


class CloudflareDetectJob(Job):
    def __init__(self):
        super().__init__("Cloudflare Detect", "cloudflare", self.cloudflare_detect)

    @staticmethod
    def cloudflare_detect(scan: Scan) -> dict:
        """Determines whether the domain is behind Cloudflare."""
        if not hasattr(CloudflareDetectJob, "ipv4_list") or not hasattr(
            CloudflareDetectJob, "ipv6_list"
        ):
            CloudflareDetectJob.ipv4_list, CloudflareDetectJob.ipv6_list = (
                CloudflareDetectJob.fetch_cloudflare_ip_lists()
            )

        ipv4_list = scan.data_dict.get("dns_records", {}).get("a", [])
        ipv6_list = scan.data_dict.get("dns_records", {}).get("aaaa", [])

        ipv4_detected = CloudflareDetectJob.is_ip_in_cloudflare_ranges(
            ipv4_list, CloudflareDetectJob.ipv4_list
        )
        ipv6_detected = CloudflareDetectJob.is_ip_in_cloudflare_ranges(
            ipv6_list, CloudflareDetectJob.ipv6_list
        )

        return {
            "ipv4": ipv4_detected,
            "ipv6": ipv6_detected,
        }

    @staticmethod
    def fetch_cloudflare_ip_lists() -> (list, list):
        """Fetches the Cloudflare IP lists for IPv4 and IPv6."""
        try:
            ipv4_list = requests.get(CF_IPV4_LIST_URL).text.splitlines()
            ipv6_list = requests.get(CF_IPV6_LIST_URL).text.splitlines()
            return ipv4_list, ipv6_list
        except requests.RequestException as e:
            print(f"Failed to fetch Cloudflare IP lists\nError: {e}")
            return [], []

    @staticmethod
    def is_ip_in_cloudflare_ranges(ip_list: list, cf_ranges: list) -> bool:
        """Checks if any IP in the list is within the Cloudflare IP ranges."""
        return any(
            any(
                ipaddress.ip_address(ip) in ipaddress.ip_network(range)
                for range in cf_ranges
                if range
            )
            for ip in ip_list
        )


def execute_command(command: str) -> list:
    """Executes a shell command and returns the output as a list of lines."""
    try:
        output = subprocess.check_output(command, shell=True).decode("utf-8").strip()
        return output.split("\n") if output else []
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {command}\nError: {e}")
        return []
