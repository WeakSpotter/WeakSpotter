import ipaddress
import subprocess
from urllib.parse import urlparse

import requests
from app.models.scan import Scan

CF_IPV4_LIST_URL = "https://www.cloudflare.com/ips-v4/"
CF_IPV6_LIST_URL = "https://www.cloudflare.com/ips-v6/"


def domain_extract(scan: Scan) -> (str, str):
    """Extracts the domain from the URL."""
    domain = urlparse(scan.url).netloc
    return "domain", domain


def execute_command(command: str) -> list:
    """Executes a shell command and returns the output as a list of lines."""
    try:
        output = subprocess.check_output(command, shell=True).decode("utf-8").strip()
        return output.split("\n") if output else []
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {command}\nError: {e}")
        return []


def dns_records(scan: Scan) -> (str, dict):
    """Retrieves the A, AAAA, and CNAME records for a domain using dig."""
    domain = scan.data_dict.get("domain")
    if not domain:
        return "dns_records", {}

    commands = {
        "a": f"dig +short {domain} A | grep '^[.0-9]*$'",
        "aaaa": f"dig +short {domain} AAAA | grep '^[0-9a-fA-F:]*$'",
        "cname": f"dig +short {domain} CNAME",
    }

    results = {key: execute_command(command) for key, command in commands.items()}
    return "dns_records", results


def whois(scan: Scan) -> (str, str):
    """Retrieves the WHOIS record for the domain."""
    domain = scan.data_dict.get("domain")
    if not domain:
        return "whois", None

    command = f"whois {domain}"
    try:
        result = subprocess.check_output(command, shell=True).decode("utf-8")
        return "whois", result
    except subprocess.CalledProcessError as e:
        print(f"WHOIS command failed for domain {domain}\nError: {e}")
        return "whois", None


def fetch_cloudflare_ip_lists() -> (list, list):
    """Fetches the Cloudflare IP lists for IPv4 and IPv6."""
    try:
        ipv4_list = requests.get(CF_IPV4_LIST_URL).text.splitlines()
        ipv6_list = requests.get(CF_IPV6_LIST_URL).text.splitlines()
        return ipv4_list, ipv6_list
    except requests.RequestException as e:
        print(f"Failed to fetch Cloudflare IP lists\nError: {e}")
        return [], []


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


def cloudflare_detect(scan: Scan) -> (str, dict):
    """Determines whether the domain is behind Cloudflare."""
    if not hasattr(cloudflare_detect, "ipv4_list") or not hasattr(
        cloudflare_detect, "ipv6_list"
    ):
        cloudflare_detect.ipv4_list, cloudflare_detect.ipv6_list = (
            fetch_cloudflare_ip_lists()
        )

    ipv4_list = scan.data_dict.get("dns_records", {}).get("a", [])
    ipv6_list = scan.data_dict.get("dns_records", {}).get("aaaa", [])

    ipv4_detected = is_ip_in_cloudflare_ranges(ipv4_list, cloudflare_detect.ipv4_list)
    ipv6_detected = is_ip_in_cloudflare_ranges(ipv6_list, cloudflare_detect.ipv6_list)

    return "cloudflare", {
        "ipv4": ipv4_detected,
        "ipv6": ipv6_detected,
    }
