import subprocess

from app.jobs.abstract_job import Job
from app.jobs.license import License


class HTTPVersionJob(Job):
    requirements = []
    key = "http_version"
    name = "HTTP Version"
    license = License.MIT

    def run(self) -> None:
        url = self._scan.url
        self.result = {}

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
                result = subprocess.run(
                    command, capture_output=True, text=True, check=True
                )

                # Check if the response contains the correct HTTP version
                supported = version in result.stdout
                self.result[version] = supported
            except subprocess.CalledProcessError as e:
                # If there's an error, mark the version as not supported and log the error
                self.result[version] = False
                print(f"Error checking {version} for {url}: {e.stderr}")
            except Exception as e:
                # Catch any other exceptions and log the error
                self.result[version] = False
                print(f"Unexpected error checking {version} for {url}: {e}")

    def parse_results(self) -> None:
        pass

    def definitions(self):
        return []
