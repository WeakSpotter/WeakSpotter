def sanitize_url(url: str) -> str:
    if not url.startswith("http"):
        url = f"https://{url}"
    return url


def add_data(scan, key, value):
    data = scan.data_dict
    data[key] = value
    scan.data_dict = data
