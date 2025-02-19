import ipaddress
from typing import Tuple

import requests
from app.jobs.abstract_job import Job
from app.jobs.license import License
from app.models.result import Result, Severity

CF_IPV4_LIST_URL = "https://www.cloudflare.com/ips-v4"
CF_IPV6_LIST_URL = "https://www.cloudflare.com/ips-v6"


class CloudflareDetectJob(Job):
    requirements = ["dns_records"]
    key = "cloudflare"
    name = "Cloudflare Detection"
    license = License.Empty

    def run(self) -> None:
        """Determines whether the domain is behind Cloudflare."""
        ipv4_list, ipv6_list = self.fetch_cloudflare_ip_lists()

        ipv4 = self._scan.data_dict.get("dns_records").get("a", [])
        ipv6 = self._scan.data_dict.get("dns_records").get("aaaa", [])

        if ipv4:
            ipv4_detected = CloudflareDetectJob.is_ip_in_cloudflare_ranges(
                ipv4, ipv4_list
            )
        else:
            ipv4_detected = False

        if ipv6:
            ipv6_detected = CloudflareDetectJob.is_ip_in_cloudflare_ranges(
                ipv6, ipv6_list
            )
        else:
            ipv6_detected = False

        self.result = {
            "ipv4": ipv4_detected,
            "ipv6": ipv6_detected,
        }

    def parse_results(self) -> None:
        pass

    def definitions(self):
        ipv4 = self._scan.data_dict.get("dns_records").get("a", [])
        ipv6 = self._scan.data_dict.get("dns_records").get("aaaa", [])

        results = []

        if ipv4 and self.result["ipv4"]:
            results.append(
                Result(
                    title="Protected by Cloudflare (IPv4)",
                    description="The domain is behind Cloudflare for IPv4.",
                    score=100,
                )
            )
        elif ipv4:
            results.append(
                Result(
                    title="Not Protected by Cloudflare (IPv4)",
                    description="The domain is not behind Cloudflare for IPv4.",
                    severity=Severity.warning,
                    score=0,
                )
            )

        if ipv6 and self.result["ipv6"]:
            results.append(
                Result(
                    title="Protected by Cloudflare (IPv6)",
                    description="The domain is behind Cloudflare for IPv6.",
                    score=100,
                )
            )
        elif ipv6:
            results.append(
                Result(
                    title="Not Protected by Cloudflare (IPv6)",
                    description="The domain is not behind Cloudflare for IPv6.",
                    severity=Severity.warning,
                    score=0,
                )
            )

        return results

    @staticmethod
    def fetch_cloudflare_ip_lists() -> Tuple[list, list]:
        """Fetches the Cloudflare IP lists for IPv4 and IPv6, caching them to files."""
        ipv4_cache_file = "cloudflare_ipv4_list.txt"
        ipv6_cache_file = "cloudflare_ipv6_list.txt"

        try:
            ipv4_list = requests.get(CF_IPV4_LIST_URL).text.splitlines()
            with open(ipv4_cache_file, "w") as f:
                f.write("\n".join(ipv4_list))

            ipv6_list = requests.get(CF_IPV6_LIST_URL).text.splitlines()
            with open(ipv6_cache_file, "w") as f:
                f.write("\n".join(ipv6_list))

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
