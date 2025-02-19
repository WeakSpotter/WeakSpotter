from app.jobs.abstract_job import Job
from app.jobs.container import run_container
from app.jobs.license import License
from app.models.result import Result, Severity

zapit_severity = {
    "Informational": Severity.info,
    "Low": Severity.warning,
    "Medium": Severity.warning,
    "High": Severity.error,
    "Critical": Severity.error,
}


class ZapitJob(Job):
    requirements = []
    key = "zapit"
    name = "Zapit"
    license = License.Apachev2

    def run(self):
        "Scan CMS site with Zapit."
        url = self._scan.url
        self.result = {}

        # Run the command in the Docker container
        self._raw_output = run_container("ghcr.io/weakspotter/zapit:latest", f"{url}")

    def parse_results(self):
        try:
            alerts_string = (
                self._raw_output.split("Number of alerts:")[1]
                .split("\n", 1)[1]
                .split("Root page stats:")[0]
            )

            print(alerts_string)

            self.result["alerts"] = [
                {
                    "severity": alert.split(": ", 1)[0].strip(),
                    "alert": alert.split(": ", 1)[1].split(" : ", 1)[0],
                    "value": alert.split(" : ", 1)[1],
                }
                for alert in alerts_string.split("\n")
                if alert
            ]
        except Exception as e:
            self.result = {"error": str(e), "raw_output": self._raw_output}

    def definitions(self):
        output = []

        for alert in self.result.get("alerts", []):
            output.append(
                Result(
                    title=alert["alert"],
                    short_description=f"{alert["alert"]} : {alert['value']}",
                    severity=zapit_severity.get(alert["severity"], Severity.info),
                )
            )

        return output
