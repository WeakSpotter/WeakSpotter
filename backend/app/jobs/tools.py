def sanitize_url(url: str) -> str:
    if not url.startswith("http"):
        url = f"https://{url}"
    return url
