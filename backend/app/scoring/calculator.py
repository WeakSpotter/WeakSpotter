from app.models.scan import Scan

# This scoring system is completely idiotic and unrealistic, but it's just an example ¯\_(ツ)_/¯


def calculate_score(scan: Scan) -> int:
    score = 100  # Start with a perfect score

    # Check HTTP status
    if (
        "http_status" in scan.data_dict
        and scan.data_dict["http_status"]["status"] >= 400
    ):
        return 0

    # Check DNS records
    dns_records = scan.data_dict.get("dns_records", {})
    if not dns_records.get("a"):
        score -= 10  # Deduct points if no A record
    if not dns_records.get("aaaa"):
        score -= 5  # Deduct points if no AAAA record
    if not dns_records.get("cname"):
        score -= 5  # Deduct points if no CNAME record

    # Check WHOIS information
    whois_info = scan.data_dict.get("whois", "")
    if "No match for domain" in whois_info:
        score -= 20  # Deduct points if WHOIS info indicates no match

    # Check Cloudflare protection
    cloudflare_info = scan.data_dict.get("cloudflare", {})
    if not cloudflare_info.get("ipv4"):
        score -= 10  # Deduct points if no Cloudflare IPv4 protection
    if not cloudflare_info.get("ipv6"):
        score -= 10  # Deduct points if no Cloudflare IPv6 protection

    # Check Nmap scan results
    nmap_info = scan.data_dict.get("nmap", {}).get("host", {})
    open_ports = nmap_info.get("ports", [])
    for port in open_ports:
        if port["state"] == "open":
            if port["portid"] == "22":
                score -= 15  # Deduct points for open SSH port
            elif port["portid"] == "80":
                score -= 10  # Deduct points for open HTTP port
            elif port["portid"] == "443":
                score -= 5  # Deduct points for open HTTPS port

    # Ensure score is within 0-100 range
    score = max(0, min(score, 100))

    return score
