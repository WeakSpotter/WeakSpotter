import subprocess

from app.jobs.abstract_job import Job
from app.jobs.license import License
from app.models.result import Result, Severity


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
        results = []

        if self.result["HTTP/1.0"]:
            results.append(
                Result(
                    title="Obsolete HTTP Version",
                    severity=Severity.warning,
                    score=-10,
                    short_description="The server supports HTTP/1.0, which is considered obsolete.",
                    description="HTTP/1.0 is an outdated version of the HTTP protocol that has been superseded by newer versions. It lacks many security features and improvements found in later versions.",
                )
            )

        if not self.result["HTTP/1.1"]:
            results.append(
                Result(
                    title="HTTP/1.1 Not Supported",
                    severity=Severity.error,
                    score=-5,
                    short_description="The server does not support HTTP/1.1.",
                    description="HTTP/1.1 is the most widely used version of the HTTP protocol. Lack of support for HTTP/1.1 may indicate an outdated or misconfigured server. 33.8% of users only have HTTP/1.1 support.",
                )
            )

        if not self.result["HTTP/2"]:
            results.append(
                Result(
                    title="HTTP/2 Not Supported",
                    severity=Severity.warning,
                    score=-5,
                    short_description="The server does not support HTTP/2.",
                    description="HTTP/2 is a major revision of the HTTP protocol that offers significant performance improvements over HTTP/1.1. Lack of support for HTTP/2 may indicate an outdated or misconfigured server. 66.2% of users have HTTP/2 support.",
                )
            )

        return results
