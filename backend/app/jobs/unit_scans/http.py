import subprocess

from app.models.scan import Scan


def version_check(scan: Scan) -> (str, dict):
    url = scan.url
    results = {}

    # Dictionary mapping HTTP versions to curl options
    version_options = {
        "HTTP/1.0": "--http1.0",
        "HTTP/1.1": "--http1.1",
        "HTTP/2": "--http2",
        # "HTTP/3": "--http3",      # Curl does not support HTTP/3 by default
    }

    for version, option in version_options.items():
        try:
            # Construct the curl command with the specified HTTP version
            command = ["curl", "-I", option, url]

            # Execute the curl command
            result = subprocess.run(command, capture_output=True, text=True)

            # Check if the response contains the correct HTTP version
            supported = version in result.stdout
            results[version] = supported
        except Exception as e:
            # If there's an error, mark the version as not supported and log the error
            results[version] = False
            print(f"Error checking {version} for {url}: {e}")

    return "http_versions", results
