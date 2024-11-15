def sanitize_url(url: str) -> str:
    if not url.startswith("http"):
        url = f"http://{url}"
    return url
